from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, DashboardView

router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')
# router.register('dashboard', DashboardView, basename='dashboard')


print(router.urls)
# urlpatterns = router.urls

urlpatterns = [

    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]


