from .models import Hobby
from django.db.models import Count, Sum, Max, F, ExpressionWrapper, DurationField
from .forms import CreateHobbyForm, SortHobbiesForm


from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse





@login_required
def create_hobby_view(request):
     create_hobby_form.user = request.user
     create_hobby_form.user_profile = request.user.userprofile
     user_profile = request.user.userprofile
     
     if request.method == "POST":
          # fill form with the user input from the request
          create_hobby_form = CreateHobbyForm(request.POST)

          # validate and process form input
          if create_hobby_form.is_valid():
               cleaned_input = create_hobby_form.cleaned_data
               name = cleaned_input['name'].lower()
               
               # create a New Hobby instance
               hobby = Hobby.objects.create(
                    user_profile=user_profile,
                    name=name,
               )
               # persist new Hobby to database
               hobby.save()

                # redirect to page showing details for the new Hobby
               return redirect("hobbies:hobby_detail", name=hobby.name)
          
          # if input is invalid, show the form again with errors
          return render(request, "hobbies/create_hobby.html", {
               "create_hobby_form": create_hobby_form
          })
     
     else:          # if request method is GET or anything else
          # create empty form for user to fill in to create a new Hobby
          create_hobby_form = CreateHobbyForm()
          return render(request, "hobbies/create_hobby.html", {
               "create_hobby_form": create_hobby_form,
          })    


     



@login_required
def hobby_detail_view(request, name):
     if request.method == "GET":
          user_profile = request.user.userprofile

          # attach the number of sessions each hobby has as a new field called 'session_count'
          # this is needed to display the number of sessions for each Hobby on its detail page
          hobbies = user_profile.hobbies.annotate(
               session_count=Count("sessions"),
          )
          # get the specific Hobby object with the given name
          hobby = hobbies.get(name=name) 

          # build the url to delete the specific Hobby
          # this is needed to pass as context to the view so the Delete Hobby button displayed on the hobby detail page works
          delete_hobby_url = reverse("hobbies:delete_hobby", args=[hobby.name])   
          

          sessions = hobby.sessions.all()                # get all sessions associated with Hobby
          sorted_sessions = sessions.order_by("-date", "-end_time")    # sort sessions by date, time in descending order (newest to oldest)
          # add a 'delete_url' attribute to each session 
          # this is needed so Delete Session button, dialog works 
          for session in sorted_sessions:
               session.delete_url = reverse("hobby_sessions:delete_session", args=[hobby.name, session.id])    # build url needed to delete Session

     
          # show page with details for specific Hobby 
          return render(request, "hobbies/hobby_detail.html", {
               "hobby": hobby,
               "delete_hobby_url": delete_hobby_url,
               "sessions": sorted_sessions,
          })
     
     return redirect("hobbies:hobby_detail", name=name)
     




@login_required
def delete_hobby_view(request, name):
     if request.method == "POST":
          hobby = get_object_or_404(Hobby, name=name, user_profile=request.user.userprofile)    # get the specific Hobby object 

          # delete the Hobby from the database
          hobby.delete()

          # redirect to the page listing all hobbies for user
          return redirect("hobbies:hobbies")










@login_required
def hobbies_view(request):
     user = request.user              # get the User that issued the request
     user_profile = user.userprofile     # get the UserProfile associated with the User
     

     # add two annotations to each Hobby in this queryset:
     #   session_count, the number of sessions associated with this hobby
     #   total_time, the sum of all session durations (total time spent on this hobby)
     hobbies = user_profile.hobbies.annotate(   
          session_count=Count("sessions"),
          total_time=Sum(
               ExpressionWrapper(
                    F("sessions__end_time") - F("sessions__start_time"),
                    output_field=DurationField()
               )
          ),
          last_session_date=Max("sessions__date")
     )


     
     if request.method == "POST":
          # fill form with the user input from the request
          sort_form = SortHobbiesForm(request.POST)

          # validate and process form input
          if sort_form.is_valid():
               choice = sort_form.cleaned_data["sort_choice"]
               order = sort_form.cleaned_data["order"]

               sort_field = "name"
               if choice == "name":
                    sort_field = "name"
               elif choice == "start_date":
                    sort_field = "date_created"
               elif choice == "number_of_sessions":
                    sort_field = "session_count"
               elif choice == "time_spent":
                    sort_field = "total_time"
               elif choice == "recent activity":
                    sort_field = "last_session_date"
                    
               if order == "desc":
                    sort_field = "-" + sort_field
               if order == "asc":
                    sort_field = sort_field.lstrip("-")

               # sort hobbies according to given sort_field
               hobbies = hobbies.order_by(sort_field)

          # show page listing all of user's hobbies, with sorting applied
          return render(request, "hobbies/hobbies.html", {
               "hobbies": hobbies,
               "sort_form": sort_form,
          })
     
     else:     # if request method is GET or anything else
          # create empty form to sort hobbies 
          sort_form = SortHobbiesForm()

          # show page listing all of user's hobbies, with ability to sort 
          return render(request, "hobbies/hobbies.html", {
               "hobbies": hobbies,
               "sort_form": sort_form,
          })
                
