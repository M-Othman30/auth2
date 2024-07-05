from django.urls import path
from .views import UserView, UserUpdateView, ChangePasswordView, RefreshTokenView

urlpatterns = [
    path('profile/', UserView.as_view(), name='user_profile'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh_token'),
]
