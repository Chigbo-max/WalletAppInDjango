
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

from wallet.models import Wallet
from .models import Profile


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'username','email', 'password', 'phone']


class ProfileSerializer(serializers.ModelSerializer):
    bvn = serializers.CharField(max_length=11, min_length=11)
    class Meta:
        model = Profile
        fields = ['user','image', 'address', 'bvn','nin']
        read_only_fields = ['user']


class WalletSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    account_number = serializers.CharField(max_length=10, read_only=True)


class DashboardSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=11, min_length=11)
    wallet = WalletSerializer()
