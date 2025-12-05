# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from src.domain.managers.user_manager import UserManager

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('architect', 'Architect'),
#         ('engineer', 'Engineer'),
#         ('client', 'Client'),
#     )

#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="client")
#     phone = models.CharField(max_length=20, blank=True)
#     is_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.username
    
#     objects = UserManager()
