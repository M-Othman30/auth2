from django.contrib.auth import get_user_model

User = get_user_model()

class UserRepository:
    def get_user_by_username(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def create_user(self, **kwargs):
        return User.objects.create_user(**kwargs)

    def save_user(self, user):
        user.save()
