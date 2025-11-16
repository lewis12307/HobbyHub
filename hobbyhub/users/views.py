from django.shortcuts import render

from django.contrib.auth.models import User
from users.models import UserProfile
from .forms import SignUpForm



def signup_view(request):
     if request.method == "POST":
          # create a form instance and fill it with the data the user submitted
          form = SignUpForm(request.POST)

          if form.is_valid():
               cleaned_input = form.cleaned_data
               first_name = cleaned_input['first_name']
               last_name = cleaned_input['last_name']
               username = cleaned_input['username']
               password = cleaned_input['password']
               bio = cleaned_input['bio']
               profile_picture = cleaned_input['profile_picture']

               user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
               user_profile = UserProfile.objects.create(user=user, bio=bio, profile_picture=profile_picture)


# form authentication
# user creation
               
# login
               
