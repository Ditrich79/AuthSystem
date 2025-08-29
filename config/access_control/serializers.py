from rest_framework import serializers
from .models import AccessRoleRule


class AccessRoleRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRoleRule
        fields = '__all__'