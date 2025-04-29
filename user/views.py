from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import mixins, request, generics, viewsets
from rest_framework.generics import CreateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from wallet.models import Wallet
from .models import Profile, User
from .serializers import ProfileSerializer, DashboardSerializer


class ProfileViewSet(ModelViewSet): #learn class based view... view sets and random routers
    permission_classes = [IsAuthenticated]
    # queryset = Profile.objects.get(user__id=request.user.id)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
        # return get_object_or_404(Profile, user__id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]


# class DashboardView(generics.ListAPIView):
# class DashboardView(viewsets.ReadOnlyModelViewSet):
class DashboardView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardSerializer

    def get_object(self):
        return self.request.user

    # def get_queryset(self):
    #     return User.objects.filter(pk=self.request.user.pk)