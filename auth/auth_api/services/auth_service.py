# auth_api/services/auth_service.py

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from .user_repository import UserRepository

class AuthService:
    _instance = None

    @staticmethod
    def get_instance():
        if AuthService._instance is None:
            AuthService()
        return AuthService._instance

    def __init__(self):
        if AuthService._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AuthService._instance = self

        self.user_repository = UserRepository()

    def obtain_token(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return {
                'access_token': access_token,
                'refresh_token': str(refresh),
                'user_type': user.user_type,
                'user_id': user.id
            }, 200  # Return response and HTTP status code
        else:
            return {'error': 'Invalid credentials'}, 401  # Return error response and HTTP status code
