from .repositories import UserRepository

class UserService:
    @staticmethod
    def change_password(user_instance, new_password):
        user_instance.set_password(new_password)
        user_instance.save()

    @staticmethod
    def get_user_profile(user_id):
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def update_user_info(user_instance, **kwargs):
        return UserRepository.update_user(user_instance, **kwargs)
