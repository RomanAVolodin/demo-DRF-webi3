from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class ProfileFeedItemSerializerShort(ModelSerializer):
    class Meta:
        model = ProfileFeedItem
        fields = ('id', 'status_text', 'created_on')


class UserProfileDetailedSerializer(ModelSerializer):
    feeds = ProfileFeedItemSerializerShort(many=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'feeds')


class ProfileFeedItemSerializer(ModelSerializer):
    """Serializes ProfileFeedItem model"""
    # user_profile = UserProfileSerializer()

    class Meta:
        model = ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        read_only_fields = ('user_profile',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT Serializer"""
    def update(self, instance, validated_data):
        super(MyTokenObtainPairSerializer, self).update(
            self, validated_data
        )  # pragma: no cover

    def create(self, validated_data):
        super(MyTokenObtainPairSerializer, self).create(
            validated_data
        )  # pragma: no cover

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.get_full_name()
        return token
