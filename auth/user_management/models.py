# # user_management/models.py

# from django.db import models
# from django.conf import settings
# from auth.auth_api import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(models.CustomUser, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True)

#     def _str_(self):
#         return f'{self.user.username} Profile'