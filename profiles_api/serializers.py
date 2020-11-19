from rest_framework import serializers

from profiles_api import models

# this is a simple serializer
class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIView"""
    # So sterilizers also take care of validation rules so if you want to say
    #you want to accept a certain field of a certain type serializers will make
    # sure that the content past that api is of the correct type that you want
    # to require for that field

    name = serializers.CharField(max_length=10)

# this is a new serializer (this is a model serializer)
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer a user profile object"""

    # this set up the serializer to point to the user model
    # first it will validate the data here
    class Meta:
        model = models.UserProfile
        #  specify a list of fields that you want to make acessible
        fields =('id','email','name','password')
        #  we want to the password right functionality
        #  we will create a dictionary with the fields that we want to pass configuration # TODO: s
        # you can only use it to create new objects or update
        # objects you can't use it to retrieve objects so when you do a get you won't
        # see the password field included in that response
        extra_kwargs = {
            'password': {
                'write_only':True,
                # costum style to it, you only see dots or starts
                'style': {'input_type':'password'}
            }
        }

    # this will overwrite the create_user function in views
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializers profile feed items"""
    # this sets our serializer or our model serializer
    # to our profile feed item model that we created in models dot py
    class Meta:
        model = models.ProfileFeedItem
        # we need to make the fields in the model available trough the serializer!
        # the ID is set up by Django by default it's automatically set to read
        # only so when you create a new object the new ID is created by the database and it is
        # set to the next available integer field or integer value in the table so just
        # increases for every object you create
        fields = ('id', 'user_profile', 'status_text', 'created_on' )
        # we want the user_profile to be read only, we do this with a dictionary 
        extra_kwargs = {'user_profile' : {'read_only':True}}
