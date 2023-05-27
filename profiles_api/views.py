import socket

from django_filters import DateTimeFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from profiles_api import serializers
from profiles_api.models import UserProfile, ProfileFeedItem
from profiles_api.permissions import UpdateOwnProfile, UpdateOwnStatus
from profiles_api.serializers import UserProfileSerializer, ProfileFeedItemSerializer, MyTokenObtainPairSerializer, UserProfileDetailedSerializer


class HelloApiView(APIView):
    serializer_class = serializers.HelloSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        my_ip = s.getsockname()[0]
        s.close()

        an_apiview = [
            f'Server ip is: {my_ip}\n',
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        a_viewset = [
            'Uses actions list, create, retrieve, update, partial_update, destroy',
            'https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions',
            'Maps maps to URL using Routers',
        ]

        return Response(a_viewset)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response({'method': f'GET {pk}'})

    def update(self, request, pk=None):
        return Response({'method': f'PUT {pk}'})

    def partial_update(self, request, pk=None):
        return Response({'method': f'PATCH {pk}'})

    def destroy(self, request, pk=None):
        return Response({'method': f'DELETE {pk}'})


class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'email')
    ordering_fields = ('name', 'email')


class FeedDateFilter(FilterSet):
    from_datetime = DateTimeFilter(field_name='feeds__created_on', lookup_expr='gte', distinct=True)
    to_datetime = DateTimeFilter(field_name='feeds__created_on', lookup_expr='lte', distinct=True)


class UserProfileDetailedListView(ListAPIView):
    serializer_class = UserProfileDetailedSerializer
    queryset = UserProfile.objects.prefetch_related('feeds').order_by('id').all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FeedDateFilter


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication, JWTAuthentication)
    permission_classes = (
        UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )
    serializer_class = ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)


class MyTokenObtainPairView(TokenObtainPairView):
    """JWT login views"""
    serializer_class = MyTokenObtainPairSerializer
