from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'role', 
            'is_active', 
            'is_verified', 
            'has_mfa', 
            'date_joined', 
            'last_login', 
            'phone', 
            'first_name', 
            'last_name'
        ]
