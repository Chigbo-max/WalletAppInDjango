from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')

print(router.urls)

urlpatterns = router.urls

