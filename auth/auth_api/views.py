from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, ObtainJWTSerializer
from .services.auth_service import AuthService
from .services.user_factory import UserFactory

class ObtainJWTView(APIView):
    def post(self, request):
        auth_service = AuthService.get_instance()
        result, status_code = auth_service.obtain_token(request)
        return Response(result, status=status_code)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        auth_service = AuthService.get_instance()
        result, status_code = auth_service.logout_user(request)
        return Response(result, status=status_code)


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user_type = self.request.data.get('user_type', 'client')  # Default to 'client' if not provided
        user_factory = UserFactory()
        user_factory.create_user(serializer.validated_data, user_type=user_type)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)