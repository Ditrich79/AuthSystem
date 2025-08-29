from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'patronymic', 'is_active', 'created']
        read_only_fields = ['created', 'is_active']


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'patronymic', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match!')
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user