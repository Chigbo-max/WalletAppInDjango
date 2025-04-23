from decimal import Decimal

import requests

from uuid import uuid4
from django.http import HttpResponse

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Transaction, Wallet

from wallet.serializers import FundSerializer, TransferFundSerializer


# Create your views here.
@api_view()
def welcome(request):
    return Response("Welcome to EaziPay")

def greeting(request, name):
    return HttpResponse(f"Hello,{name}")

def second_greeting(request, name):
    return render(request, 'hello.html', {'name': name})
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def fund_wallet(request):
    try:
        data=FundSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        amount = data.validated_data['amount']
        amount*= 100
        email = request.user.email
        reference = f'ref_{uuid4().hex}'

        Transaction.objects.create(
            amount=(amount/100),
            reference=reference,
            sender =  request.user,
            )

        url = 'https://api.paystack.co/transaction/initialize'

        secret = settings.PAYSTACK_SECRET_KEY
        headers = {
            "Authorization": f"Bearer {secret}",
        }

        data = {
            "amount": amount,
            "reference": reference,
            "email": email,
            "callback_url": "http://localhost:8000/wallet/fund/verify"
        }

        response_str = requests.post(url=url, json=data, headers=headers) #the api call
        response = response_str.json()
        if response['status']:
            return Response(data=response['data'], status=status.HTTP_200_OK)
        return Response({"message": "Unable to complete transactions"}, status=status.HTTP_302_FOUND)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""
curl https://api.paystack.co/transaction/initialize 
-H "Authorization: Bearer YOUR_SECRET_KEY"
-H "Content-Type: application/json"
-X POST
"""


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def verify_fund(request):
    reference = request.GET.get('reference')
    secret = settings.PAYSTACK_SECRET_KEY

    headers = {
        "Authorization": f"Bearer {secret}",
    }

    url =f'https://api.paystack.co/transaction/verify/{reference}'
    response_str = requests.get(url=url, headers=headers)
    response = response_str.json()
    if response['status'] and response['data']['status'] == 'success': #instead of ['data'].get('Status')
        amount =  (response['data']['amount']/100)
        try:
            transaction = Transaction.objects.get(reference=reference, verified=False)
        except Transaction.DoesNotExist:
            return Response({"message": "Transaction does not exist"}, status=status.HTTP_404_NOT_FOUND)

        wallet = get_object_or_404(Wallet, user=request.user) #django's shortcut to get from model, instead of try and catch
        wallet.deposit(Decimal(amount))
        transaction.verified = True
        transaction.save()
        return Response({"message": "Transaction successfully verified"}, status=status.HTTP_200_OK)
    return Response({"message": "Unable to verify transaction"}, status=status.HTTP_400_BAD_REQUEST)
        # return Response(data=response['data'], status=status.HTTP_200_OK)


"""
curl https://api.paystack.co/transferrecipient 
-H "Authorization: Bearer YOUR_SECRET_KEY"
-H "Content-Type: application/json"
-X POST
"""

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def make_transfer_to_another_wallet(request):
    data = TransferFundSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    amount = data.validated_data['amount']
    recipient_account_number = data.validated_data['account_number']
    reference = f'ref_{uuid4().hex}'

    try:
       sender_wallet = Wallet.objects.get(user=request.user)
       receiver_wallet = Wallet.objects.get(account_number=recipient_account_number)

       if sender_wallet.balance < amount:
           return Response({"message": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

       if sender_wallet == receiver_wallet:
           return Response({"message":"You cannot make transfer to yourself"}, status=status.HTTP_400_BAD_REQUEST)
       
       sender_wallet.balance -= amount
       receiver_wallet.balance += amount

       Transaction.objects.create(
           reference=reference,
           amount=amount,
           sender=request.user,
           receiver_id=receiver_wallet.id,
           transaction_type='T',
           verified=True
       )

       sender_wallet.save()
       receiver_wallet.save()

       return Response({"message": f"Transfer to {recipient_account_number} was successful", "reference": f"{reference}"
                                , "new balance": f'{sender_wallet.balance}' }, status=status.HTTP_200_OK)

    except Wallet.DoesNotExist:
        return Response({"message": "Wallet does not exist"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
