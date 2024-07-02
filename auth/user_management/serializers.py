# user_management/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=User.USER_TYPES)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'user_type')  # Include user_type in the fields

class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=User.USER_TYPES)

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'user_type')  # Include user_type in the fields

class UserUpdateSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=User.USER_TYPES)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type')  # Include user_type in the fields

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
