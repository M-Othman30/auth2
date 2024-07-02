# auth_api/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from .serializers import UserRegistrationSerializer, ObtainJWTSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class ObtainJWTView(APIView):
    def post(self, request):
        serializer = ObtainJWTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
           
            return Response({
               'access_token': access_token,
                'refresh_token': str(refresh),
                'user_type': user.user_type  # Include user_type in the response
            }, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                refresh_token.blacklist()
                return Response({'message': 'Successfully logged out'})
            except:
                return Response({'message': 'Invalid token'}, status=401)

        logout(request)
        return Response({'message': 'Successfully logged out'})

class RegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user_type = self.request.data.get('user_type', 'client')  # Set a default if not provided
        serializer.save(user_type=user_type)


