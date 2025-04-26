from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import mixins, request
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .serializers import ProfileSerializer

class ProfileViewSet(ModelViewSet): #learn class based view... view sets and random routers
    permission_classes = [IsAuthenticated]
    # queryset = Profile.objects.get(user__id=request.user.id)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
        # return get_object_or_404(Profile, user__id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)