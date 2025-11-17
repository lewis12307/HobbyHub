from django.db import models
from django.contrib.auth.models import User


# Extend Django's built-in User model to have extra profile information
class UserProfile(models.Model):
    # Connect profile to a single User. Each User has exactly one UserProfile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)  

    # Django's User model already includes: username, password, email, first_name, last_name, is_active, last_login, and date_joined.
    # Additional custom fields that do NOT exist on Django's User model
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)   # image for the user's profile --- optional; if provided, saved to media/profile_pictures/

