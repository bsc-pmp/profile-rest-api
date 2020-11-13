from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """Test API View"""
    # retrieve a list of objects of specify object
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLS',
        ]

        return Response({'messsage':'Hello', 'an_apiview':an_apiview})
