from rest_framework.views import APIView
from rest_framework.response import Response
# serializers imports
from rest_framework import status

from profiles_api import serializers


class HelloApiView(APIView):
    """Test API View"""
    # tell apiview what data to expect when making request or post ...expect name max length of 10
    serializer_class = serializers.HelloSerializer

    # retrieve a list of objects of specify object
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLS',
        ]

        return Response({'message':'Hello', 'an_apiview':an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        # retrieve the serializer and pass the data from the request
        # standard way to retrieve serializer in a view
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            # when you use the f you can insert data into your code{}
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            # this is good for who is using api know what went wrong
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Handle updating and object"""
        # we make a http we make to specific a prmiary key but with None in case we don't want
        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        # the patch only updated the fields provided in the request!
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})
