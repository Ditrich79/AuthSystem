from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer, RegisterSerializer
from ..utils import generate_jwt


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_jwt(user.id)
        return Response({'token': token}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'Account deactivated'}, status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):
    def post(self, request):
        return Response({'message': "Logged out"})