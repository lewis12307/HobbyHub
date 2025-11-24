from django.contrib.auth.models import User
from accounts.models import UserProfile

from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm, EditProfileForm

from django.views.decorators.cache import never_cache





from django.contrib import messages

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse





@never_cache
# @never_cache forces the browser to always fetch a fresh copy of the form.
# Without this, using the Back button after signup/login can load a stale version of the page containing an old CSRF token, which causes"CSRF token incorrect" errors when the form is resubmitted.
def signup_view(request):
     if request.method == "POST":
          # create a form instance and fill it with the data the user submitted
          signup_form = SignUpForm(request.POST, request.FILES)

          # validate and process form input
          if signup_form.is_valid():
               cleaned_input = signup_form.cleaned_data
               first_name = cleaned_input['first_name'].title()
               last_name_input = cleaned_input['last_name']
               if last_name_input:
                    last_name = last_name_input.title()
               else:
                    last_name = ""
               username = cleaned_input['username']
               password = cleaned_input['password']
               bio_input = cleaned_input['bio']
               if bio_input:
                    bio = bio_input
               else:
                    bio = None
               profile_picture_input = cleaned_input['profile_picture']
               if profile_picture_input:
                    profile_picture = profile_picture_input
               else:
                    profile_picture = None

               # create new User instance
               user = User.objects.create_user(
                    username=username, 
                    password=password, 
                    first_name=first_name, 
                    last_name=last_name
               )
               # persist User to database
               user.save()   

               # create new UserProfile instance
               user_profile = UserProfile.objects.create(
                    user=user, 
                    bio=bio,
                    profile_picture=profile_picture
               )
               # persist UserProfile to database
               user_profile.save()    
               
               # display a success message so the user knows their profile was created
               messages.success(request, "Yay! Your profile is all set.")

               # login in the new user
               login(request, user)
               # redirect user to their dashboard, featuring notifications
               return redirect("dashboard")

          # If input is invalid, notify user and show signup form again with errors
          return render(request, "accounts/signup.html", {"signup_form": signup_form})
     

     else:        # if request is GET or anything else
          # create a blank signup form for user to fill in
          signup_form = SignUpForm()   

          # render the template and show the empty signup form to the user
          return render(request, "accounts/signup.html", {"signup_form": signup_form})
     





@never_cache
# @never_cache forces the browser to always fetch a fresh copy of the form.
# Without this, using the Back button after signup/login can load a stale version of the page containing an old CSRF token, which causes"CSRF token incorrect" errors when the form is resubmitted.
def login_view(request):
     if request.method == "POST":
          # create a form instance and fill it with the data the user submitted
          login_form = LoginForm(request.POST)     

          # validate and process form input
          if login_form.is_valid():
               cleaned_input = login_form.cleaned_data
               username = cleaned_input["username"]
               password = cleaned_input["password"]

               # authenticate user  --- check if the provided username and password match for an existing user account
               user = authenticate(request, username=username, password=password)

               # if the user exists and login credentials are correct, login the user
               if user:
                    login(request, user)
                    return redirect("dashboard")   
               # attach an error message to the form if authentication fails and display it to user
               elif user is None:
                    login_form.add_error("username", "Hmm… something didn’t match. Please try entering your username and password again.")
                    login_form.add_error("password", "Hmm… something didn’t match. Please try entering your username and password again.")

          # if input is not valid or authentication failed, show login form again with errors
          return render(request, "accounts/login.html", {"login_form": login_form})
     
     else:         # if request is GET or anything else
          # create a blank login form for user to fill in
          login_form = LoginForm()   

          # render the template and show the empty login form to the user
          return render(request, "accounts/login.html", {"login_form": login_form})





def profile_view(request, username):
     if request.method == "GET":
          if request.user.is_authenticated:   # check if user is logged in currently
               #user = request.user
               user = User.objects.get(username=username)
               user_profile = user.userprofile     # access the UserProfile linked to the User
               hobbies = user_profile.hobbies.all()    # get all Hobbies for that UserProfile

               delete_url = reverse("accounts:delete")
               return render(request, "accounts/profile.html", {
                    "user": user,
                    "profile": user_profile,
                    "delete_url": delete_url,
                    "hobbies": hobbies
               })          
          # if user is not logged in, redirect them to login page
          else:
               return redirect('accounts:login') 
          
          # if request.user.username != username:



def logout_view(request):
     if request.method == "POST":
          # logout user
          logout(request)

          # redirect user back to login page 
          return redirect("accounts:login")          



def edit_profile_view(request, username):
     user = request.user
     profile = user.userprofile

     if request.method == "GET":
          current_profile_info = {
               "first_name": user.first_name,
               "last_name": user.last_name,
               "username": user.username,
               "password": user.password,
               "bio": profile.bio,
               "profile_picture": profile.profile_picture,
          }
          edit_profile_form = EditProfileForm(initial=current_profile_info)
          return render(request, "accounts/edit_profile.html", {"edit_profile_form": edit_profile_form})
     
     # if request.method == "POST":
     #      pass



def delete_profile_view(request):
     if request.method == "POST":
          user = request.user
          profile = user.userprofile

          # delete User, UserProfile from database 
          user.delete()
          # profile.delete()    # do not need to delete profile manually because of on_delete=models.CASCADE on User
          
          # redirect user back to login page 
          return redirect("accounts:login") 