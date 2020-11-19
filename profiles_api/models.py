from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# class59
from django.conf import settings

# Create your models here.
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """"Create a New user profile"""
        if not email:
            raise ValueError('User must have an email address')
        # normalize the email address, case sensitive, the second half
        email = self.normalize_email(email)
        # create the user model, create a new model
        user = self.model(email=email, name=name)
        # make sure the password is increpited...not plain text in the database
        user.set_password(password)
        # save the database
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    # unique don't allow two users to use the same field
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # determine if the user is activated---true or false value
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # specify the model manager costum model manager, create and control users
    objects = UserProfileManager()

    # overwrite instead name is email to enter in required field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['name']

    def get_full_name(self):
        """retrieve full name of use"""
        return self.name

    def get_short_name(self):
        """retrieve short name o user"""
        return self.name

    # now the string representation of the model

    def __str__(self):
        """return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update
    he way you link models to other models in Django is
    you use what's called a foreign key when you use the foreign key field it sets up
    a foreign key relationship in the database to a remote model
    the benefit of doing this is that it allows you to ensure that the integrity
    of the database is maintained so you can never create a profile feed item for a
    user profile that doesn't exist so let's go ahead and add our user profile field
    to our profile feed item"""
    #  the first argument of a foreign key field in models is the name
    # of the model that is the remote model for thisforeign key
    # what this will do is it will retrieve the value
    # from the author user model setting in our settings dot py file so if we ever
    # swap this auth user model to a different model then the relationships
    # will automatically be updated without us having to go through and manually change
    # it everywhere that we've referenced it in our models dot py

    # what the on delete does is it tells Django or it
    # tells the database what to do if the remote field is deleted so we have user
    # we have profile feed items in our database and each one of them has a user
    # profile associated with it now because there's a foreign key Association the
    # database needs to know what happens if you remove a user profile what should
    # happen to the profile feed items that are associated with it and the way you
    # do that is by specifying this on delete so there are different things that you
    # can set on delete one of them is cascade and what that does is it says basically
    # cascade the changes down through all the related fields so if you have user
    # profile feed items associated to a user profile and you remove that profile then
    # it will cascade the change down and remove the associated feed items from
    # that user


    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a strings"""
        return self.status_text
