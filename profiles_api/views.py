from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from profiles_api import serializers
from profiles_api.models import UserProfile
from profiles_api.permissions import UpdateOwnProfile
from profiles_api.serializers import UserProfileSerializer


class HelloApiView(APIView):
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        an_apiview = [
            'Uses HTTP methods',
            'Is similar to traditional Django view',
            'Gives you the most control over your app logic',
            'Is mapped manually to URLs',
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

