# auth_api/urls.py

from django.urls import include, path
from .views import ObtainJWTView, LogoutView, RegistrationView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('api/token/', ObtainJWTView.as_view(), name='token_obtain_pair'),
    path('api/logout/', LogoutView.as_view(), name='logout_view'),
    path('api/register/', RegistrationView.as_view(), name='register_view'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),





    
]
