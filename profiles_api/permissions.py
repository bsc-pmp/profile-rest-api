from rest_framework import permissions

# class 51
# allow users to edit their own profile this is what this permission is going to
# allow the users to do the way you define permission classes is you add a has
# object permissions function to the class which gets called every time a request
# is made to the API that we assign our permission to this function
# will return a true or a false to determine whether the authenticated user
# has the permission to do the change they're trying to do

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile """
    # allow or denie these changes
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile """
        if request.method in permissions.SAFE_METHODS:
            return True
        # True if the user is updtaing their profile
        # What we're going to do is we're
        # going to check whether the object they're updating matches their
        #authenticated user profile that is added to the authentication of the request so
        #when you authenticate a request in Django rest framework it will assign the
        #authenticated user profile to the request and we can use this to compare
        #it to the object that is being updated and make sure they have the same ID

        return obj.id == request.user.id
