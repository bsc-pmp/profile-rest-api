from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

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
