from rest_framework.views import APIView
from rest_framework.response import Response
# serializers imports
from rest_framework import status
###  viewssets
from rest_framework import viewsets
# class 52
from rest_framework.authentication import TokenAuthentication
#  class 54
from rest_framework import filters
# class 55
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# class 65
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# class 67 - this block the user if is not authenticated
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
# class 48
from profiles_api import models
#  class 52 - read only if user not authenticated
from profiles_api import permissions

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

# views set that rest api provide
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    # we can share the same serializer
    serializer_class=serializers.HelloSerializer

    def list(self, request):
        """ Return a hello message"""
        a_viewset =[
            'Uses actions (list, create, retrieve, update, partial_update )',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response ({'message':'Hello!', 'a_viewset': a_viewset})


    def create(self, request):
        """ Create a new hello message"""
        #  THE SERIALIZER CLASS IS specifIED IN THE Serializer.PY
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message =f'Hello {name}!'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    #  retrieve a specific oject with pk
    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID."""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handles updating an object."""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handles updating part of an object."""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None, primary_key=False):
        """Handles removing an object"""

        return Response({'http_method':'DELETE'})

# the way you use a model view set is you connect it up to a
# serializer class just like you would a regular view set and you provide a query
# set to the model view set so it knows which objects in the database are going
# to be managed through this view set

class UserProfileViewSet(viewsets.ModelViewSet):
    """" Handle creating and updating pofiles
    The Django rest framework knows the standard functions that you would want to perform
    on a model view set and that is the create function to create new items the
    list function to list the models that are in the database
    the update partial update and destroy to manage specific model objects in the
    database Django rest framework takes care of all of this for us
    just by assigning the serializer class to a model serializer
    and the query set this is the great thing about the Model View set"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    # class 52
    authentication_classes = (TokenAuthentication,)
    # premission on profile, to see if the user have permissions
    permission_classes = (permissions.UpdateOwnProfile,)
    # class 54
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    #  we need to adapt to be visibilie in the browser
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    # this set the serializer class to the profile feed in the serializar.property
    serializer_class = serializers.ProfileFeedItemSerializer
    # we're going to manage all of our profile feed item objects from our model in our view set
    queryset = models.ProfileFeedItem.objects.all()
    # class 65
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated,
        # IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        """sets the user profile to the logged in user"""
        # sets the user profile to the logged in user the perform create

        # function is a handy feature of the Django rest framework that allows you to
        # override the behavior or customize the behavior for creating objects through a
        # Model View set so when a request gets made to our view set it gets passed into
        # our serializer class and validated and then the serializer dot save function is
        # called by default if we need to customize the logic for creating an
        # object then we can do this using the perform create function so this perform
        # create function gets called every time you do an HTTP POST to our view set

        serializer.save(user_profile=self.request.user)
