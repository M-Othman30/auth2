from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, UserUpdateSerializer, ChangePasswordSerializer
from .services.services import UserService
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'detail': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)

        UserService.change_password(user, serializer.validated_data['new_password'])

        return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return UserService.get_user_profile(self.request.user.id)

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = UserService.update_user_info(user, **serializer.validated_data)

        return Response({"message": "User information updated successfully"}, status=status.HTTP_200_OK)

class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = RefreshToken.for_user(request.user)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token, 'refresh_token': str(refresh), 'user_type': request.user.user_type})
