from django.contrib.auth.models import User
from accounts.models import UserProfile

from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm

from django.contrib import messages

from django.shortcuts import render
from django.shortcuts import redirect






def signup_view(request):
     if request.method == "GET":
           # create a blank signup form for user to fill in
          form = SignUpForm()   

           # render the template and show the empty signup form to the user
          return render(request, "signup.html", {"form": form})    


     if request.method == "POST":
          # create a form instance and fill it with the data the user submitted
          form = SignUpForm(request.POST, request.FILES)

          # validate and process form input
          if form.is_valid():
               cleaned_input = form.cleaned_data
               first_name = cleaned_input['first_name'].title()
               last_name = cleaned_input['last_name']
               if last_name:
                    last_name = last_name.title()
               username = cleaned_input['username']
               password = cleaned_input['password']
               bio = cleaned_input['bio']
               profile_picture = cleaned_input['profile_picture']

               # create new User and UserProfile objects
               user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
               user_profile = UserProfile.objects.create(user=user, bio=bio, profile_picture=profile_picture)
               
               # display a success message so the user knows their profile was created
               messages.success(request, "Yay! Your profile is all set.")

               # login in the new user
               login(request, user)
               return redirect("home")

          # If input is invalid, notify user and show signup form again with errors
          messages.error(request, "We couldn’t create your profile just yet. It looks like a few details need another look.")
          return render(request, "signup.html", {"form": form})
     




def login_view(request):
    if request.method == "GET":
          # create a blank login form for user to fill in
          form = LoginForm()   

          # render the template and show the empty login form to the user
          return render(request, "login.html", {"form": form})
    

    if request.method == "POST":
          # create a form instance and fill it with the data the user submitted
          form = LoginForm(request.POST)     

          # validate and process form input
          if form.is_valid():
               cleaned_input = form.cleaned_data
               username = cleaned_input["username"]
               password = cleaned_input["password"]

               # authenticate user  --- check if the provided username and password match for an existing user account
               user = authenticate(request, username=username, password=password)

               # if the user exists and login credentials are correct, login the user
               if user:
                    login(request, user)
                    return redirect("home")    # may have to change
               # display an error message if authentication fails 
               elif user is None:
                    form.add_error(None, "Hmm… something didn’t match. Please try entering your username and password again.")

          # if input is not valid or authentication failed, show login form again with errors
          return render(request, "login.html", {"form": form})


# logout                
