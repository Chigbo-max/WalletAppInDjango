"""
URL configuration for eaziPay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path, include


admin.site.site_header = 'EaziPay Admin'
# admin.site.site_title = 'EaziPay Admin Portal'
admin.site.index_title = 'EaziPay Admin Portal'


schema_view = get_schema_view(
   openapi.Info(
      title="Smart Pay Docs",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=([permissions.AllowAny,]),
)


urlpatterns = [
       path('admin/', admin.site.urls),
        path('wallet/', include('wallet.urls')),
        path('user/', include('user.urls')),


        path('auth/', include('django.contrib.auth.urls')),

        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.jwt')),

# http://127.0.0.1:8000/api/docs/swagger/

 path('api/docs/swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
 path('api/docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
 path('api/docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
