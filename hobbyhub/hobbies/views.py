from .models import Hobby
from .forms import CreateHobbyForm, SortHobbiesForm
from django.db.models import Count, Sum, Max, F, ExpressionWrapper, DurationField


from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse




def create_hobby_view(request):
     if request.method == "GET":
          # create empty form for user to fill in to create a new Hobby
          form = CreateHobbyForm()
          return render(request, "hobbies/create_hobby.html", {"form": form})    


     if request.method == "POST":
          # fill form with the user input from the request
          form = CreateHobbyForm(request.POST)
          form.user = request.user
          form.user_profile = request.user.userprofile
          user_profile = request.user.userprofile

          # validate and process form input
          if form.is_valid():
               cleaned_input = form.cleaned_data
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
          return render(request, "hobbies/create_hobby.html", {"form": form})
     



def hobby_detail_view(request, name):
     if request.method == "GET":
          hobby = get_object_or_404(Hobby, name=name, user_profile=request.user.userprofile)     # retrieve the Hobby object 
          delete_url = reverse("hobbies:delete_hobby", args=[hobby.name])   # build the url to delete the specific Hobby

          sessions = hobby.sessions.all()
          sorted_sessions = sessions.order_by("-date", "-end_time")    # sort sessions by date, time in descending order (newest to oldest)

          # show page with info for single specific Hobby 
          return render(request, "hobbies/hobby_detail.html", {
               "hobby": hobby,
               "delete_url": delete_url,
               "sessions": sorted_sessions,
          })




def delete_hobby_view(request, name):
     if request.method == "POST":
          hobby = get_object_or_404(Hobby, name=name, user_profile=request.user.userprofile)    # retrieve the Hobby object 

          # delete the Hobby from the database
          hobby.delete()

          # redirect to the page listing all hobbies for user
          return redirect("hobbies:hobbies")











def hobbies_view(request):
     user = request.user             # get the User that issued the request
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



     if request.method == "GET":
          # create empty form to sort hobbies 
          sort_form = SortHobbiesForm()

          # show page listing all of user's hobbies, with ability to sort 
          return render(request, "hobbies/hobbies.html", {
               "hobbies": hobbies,
               "sort_form": sort_form,
          })
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

               hobbies = hobbies.order_by(sort_field)

          # show page listing all of user's hobbies, with sorting applied
          return render(request, "hobbies/hobbies.html", {
               "hobbies": hobbies,
               "sort_form": sort_form,
          })
                
