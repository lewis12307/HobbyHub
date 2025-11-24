from hobbies.models import Hobby
from hobby_sessions.models import Session

from .forms import CreateSessionForm, EditSessionForm

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect






def create_session_view(request, hobby_name):
     user = request.user
     user_profile = user.userprofile
     hobby = get_object_or_404(Hobby, name=hobby_name, user_profile=user_profile)

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
               friend_visibility = cleaned_input["friend_visibility"]


               # create a new Session instance
               session = Session.objects.create(
                    user_profile=user_profile,
                    hobby=hobby,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    description=description,
                    upload=upload,
                    friend_visibility=friend_visibility,
               )
               # persist new Session to database
               session.save()

               # redirect to page showing details for the Hobby
               return redirect("hobbies:hobby_detail", name=hobby.name)

          # if input is not valid, show form again with errors
          return render(request, "hobby_sessions/create_session.html", {
               "hobby": hobby, 
               "create_session_form": create_session_form,
          })
     
     else:        # f method is GET or anything else
          # create empty form for user to fill in to create a session for a specific Hobby 
          create_session_form = CreateSessionForm()

          # show page listing all of user's hobbies, with ability to sort 
          return render(request, "hobby_sessions/create_session.html", {
               "hobby": hobby, 
               "create_session_form": create_session_form,
          })
     




def delete_session_view(request, hobby_name, session_id):
     user = request.user
     user_profile = user.userprofile

     session = get_object_or_404(
          Session,
          id=session_id,
          hobby__name=hobby_name,
          hobby__user_profile=user_profile
     )
     
     if request.method == "POST":
          # delete the Session from the database
          session.delete()

          return redirect("hobbies:hobby_detail", name=hobby_name)




def edit_session_view(request, hobby_name, session_id):
     # get required information in order to get correct session object
     user = request.user
     user_profile = user.userprofile
     hobby = get_object_or_404(Hobby, user_profile=user_profile, name=hobby_name)

     # get specific session object and its current information
     session = get_object_or_404(Session,  user_profile=user_profile, hobby=hobby, id=session_id)
     current_date = session.date
     current_start_time = session.start_time
     current_end_time = session.end_time
     current_description = session.description
     current_upload = session.upload
     current_friend_visibility = session.friend_visibility

     if request.method == "POST":
          # create a form instance and fill it with the data the user submitted
          edit_session_form = EditSessionForm(request.POST)  

          # validate and process form input
          if edit_session_form.is_valid():
               cleaned_input = edit_session_form.cleaned_data
               new_date = cleaned_input["date"]
               new_start_time = cleaned_input["start_time"]
               new_end_time = cleaned_input["end_time"]
               new_description = cleaned_input["description"]
               new_upload = cleaned_input["upload"]
               new_friend_visibility = cleaned_input["friend_visibility"]

               if new_date != current_date:
                    session.date = new_date
               if new_start_time != current_start_time:
                    session.start_time = new_start_time
               if new_end_time != current_end_time:
                    session.end_time = new_end_time
               if new_description != current_description:
                    session.description = new_description
               if new_upload != current_upload:
                    session.upload = new_upload
               if new_friend_visibility != current_friend_visibility:
                    session.friend_visibility = new_friend_visibility
               session.save()

               # redirect user back to hobby detail page 
               return redirect("hobbies:hobby_detail", name=hobby_name)  

          # if input is invalid, show the form again with errors
          return render(request, "hobby_sessions/edit_session.html", {
               "edit_session_form": edit_session_form,
               "hobby": hobby,
          })



     else:      # if request method is GET or anything else
          current_session_info = {
               "date": session.date,
               "start_time": session.start_time,
               "end_time": session.end_time,
               "description": session.description,
               "upload": session.upload,
               "friend_visibility": session.friend_visibility,
          }
          # fill in form with the current info in the user's profile
          edit_session_form = EditSessionForm(initial=current_session_info)
          return render(request, "hobby_sessions/edit_session.html", {
               "edit_session_form": edit_session_form,
               "hobby": hobby,
          })