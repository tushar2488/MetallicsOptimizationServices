"""metallics_services_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from metallics_api import views
from .api import router
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/get_comodity_details/<int:id>/', views.GetComodityDetail.as_view(), name='get_comodity_details'),
    path('api/v1/update_comodity_details/', views.UpdateComodityDetail.as_view(), name='update_comodity_details'),
    path('api/v1/remove_chemical_composition/', views.RemoveChemicalComposition.as_view(), name='remove_chemical_composition'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/v1/', include(router.urls)),
]
