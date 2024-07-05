# auth_api/services/user_factory.py

from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory:
    @staticmethod
    def create_user(validated_data, user_type='client'):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            user_type=user_type
        )
