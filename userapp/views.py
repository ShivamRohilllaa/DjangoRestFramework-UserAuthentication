from django.shortcuts import render
from .models import Student
from .serializers import UserSignupSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your views here.


@api_view(['POST'])
def signup(request):
    data = request.data
    serializer = UserSignupSerializer(data=data)
    if serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], username=data['email'], email=data['email'], password=make_password(data['password']))
            user.save()
            student = Student.objects.create(auth=user, name=data['first_name'], email=data['email'])
            return Response({'message':'User Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'User Already Exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def login(request):
    data = request.data
    if User.objects.filter(username=data['email']).exists():
        user = User.objects.get(username=data['email'])
        if user.check_password(data['password']):
            return Response(UserSerializer(instance=user).data, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message':'User Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)

