from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import UserSerializer
from rest_auth.serializers import TokenSerializer

from django.contrib.auth.models import User
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer;
    queryset = User.objects.all();

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def login(self,request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        resp = { 
            'user' : user.username,
        }
        return Response(resp, status=200)

    def create(self, request):
        self.login(request)


#    def create(self, request):
#        password = request.data['password']
#        serializer = UserSerializer(data = request.data)
#        serializer.is_valid(raise_exception=True)
#        
#        user = serializer.save()
#        user.set_password(password)
#        user.save()
#
#        return Response(serializer.data)

