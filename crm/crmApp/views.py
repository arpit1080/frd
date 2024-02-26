from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from crmApp.serializers import UserSignUpSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from crmApp.models import User
from django.shortcuts import get_object_or_404



@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        data = request.data
        serializer = UserSignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=400)

            # Check if the provided password matches the user's password
            if check_password(password, user.password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'message': 'Login successful'})
            else:
                return Response({'error': 'Invalid username or password'}, status=400)

        return Response(serializer.errors, status=400)
