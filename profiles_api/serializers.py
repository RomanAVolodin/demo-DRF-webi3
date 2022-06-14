from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from profiles_api.models import UserProfile, ProfileFeedItem


class HelloSerializer(Serializer):
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(ModelSerializer):
    """Serializes UserProfile model"""

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        user = UserProfile.objects.create(
            email=validated_data['email'], name=validated_data['name'], password=validated_data['password']
        )
        return user


class ProfileFeedItemSerializer(ModelSerializer):
    """Serializes ProfileFeedItem model"""
    # user_profile = UserProfileSerializer()

    class Meta:
        model = ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        read_only_fields = ('user_profile',)

