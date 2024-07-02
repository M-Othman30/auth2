# user_management/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, UserUpdateSerializer, ChangePasswordSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

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

        # Check if the provided old password is correct
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'detail': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)


class UserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        queryset = User.objects.get(pk=self.request.user.id)
        return queryset 
    


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "User information updated successfully"}, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = RefreshToken.for_user(request.user)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token, 'refresh_token': str(refresh), 'user_type': request.user.user_type})
