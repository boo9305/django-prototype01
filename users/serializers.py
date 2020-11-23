from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
    
    def create(self, validate_data):
        password = validate_data['password']
        user = User.objects.create(**validate_data)
        user.set_password(password)
        user.save()

        return user


