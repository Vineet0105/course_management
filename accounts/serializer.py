from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
import re
from rest_framework.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,write_only=True,
                                   validators = [UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True,
                                     validators = [UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length = 6,write_only =True)

    def validate_password(self, value):
        # Minimum password length check is already done by DRF
        
        # Check if password contains at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # Check if password contains at least one digit
        if not re.search(r'[0-9]', value):
            raise ValidationError("Password must contain at least one number.")

        # Check if password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("Password must contain at least one special character.")

        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'],
                                        email = validated_data['email'],
                                        password = validated_data['password'])
        return user
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        