from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    def get(self, request, format=None):
        an_apiview = [
            'Users HTTM methods',
            'Is similar to traditional Django view',
            'gives you the most control over your app logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})
