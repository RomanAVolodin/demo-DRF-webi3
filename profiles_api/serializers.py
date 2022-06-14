from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from profiles_api.models import UserProfile


class HelloSerializer(Serializer):
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(ModelSerializer):
    """Serialises UserProfile model"""

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        user = UserProfile.objects.create(
            email=validated_data['email'], name=validated_data['name'], password=validated_data['password']
        )
        return user
