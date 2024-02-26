from rest_framework import serializers
from crmApp.models import User
from django.contrib.auth.hashers import make_password


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'address', 'dob', 'role', 'mobile_number', 'profile_photo']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        # Remove confirm_password field before saving
        validated_data.pop('confirm_password', None)
        return super().create(validated_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
