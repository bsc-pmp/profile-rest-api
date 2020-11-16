from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIView"""
    # So sterilizers also take care of validation rules so if you want to say
    #you want to accept a certain field of a certain type serializers will make
    # sure that the content past that api is of the correct type that you want
    # to require for that field

    name = serializers.CharField(max_length=10)
