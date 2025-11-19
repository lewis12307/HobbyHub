from hobbies.models import Hobby
from hobby_sessions.models import Session

from .forms import CreateSessionForm

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect






def create_session_view(request, hobby_name):
     user = request.user
     user_profile = user.userprofile
     hobby = get_object_or_404(Hobby, name=hobby_name, user_profile=user_profile)

     if request.method == "GET":
          # create empty form for user to fill in to create a session for a specific Hobby 
          create_session_form = CreateSessionForm()

          # show page listing all of user's hobbies, with ability to sort 
          return render(request, "hobby_sessions/create_session.html", {
               "hobby": hobby, 
               "create_session_form": create_session_form,
          })
     
     if request.method == "POST":
           # fill form with the user input from the request
          create_session_form = CreateSessionForm(request.POST, request.FILES)


          # validate and process form input
          if create_session_form.is_valid():
               cleaned_input = create_session_form.cleaned_data
               date = cleaned_input["date"]
               start_time = cleaned_input["start_time"]
               end_time = cleaned_input["end_time"]
               description = cleaned_input["description"]
               upload = cleaned_input["upload"]
               friend_visibiilty = cleaned_input["friend_visibiilty"]


               # create a new Session instance
               session = Session.objects.create(
                    user_profile=user_profile,
                    hobby=hobby,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    description=description,
                    upload=upload,
                    friend_visibiilty=friend_visibiilty,
               )
               # persist new Session to database
               session.save()

               # redirect to page showing details for the Hobby
               return redirect("hobbies:hobby_detail", name=hobby.name)

          # if input is not valid, show form again with errors
          return render(request, "hobby_sessions/create_session.html", {"create_session_form": create_session_form})

