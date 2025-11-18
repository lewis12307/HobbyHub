from .models import Hobby
from .forms import CreateHobbyForm

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse






def create_hobby_view(request):
     if request.method == "GET":
          form = CreateHobbyForm()
          return render(request, "hobbies/create_hobby.html", {"form": form})    


     if request.method == "POST":
          form = CreateHobbyForm(request.POST)
          form.user = request.user

          # validate and process form input
          if form.is_valid():
               cleaned_input = form.cleaned_data
               name = cleaned_input['name'].lower()
               
               hobby = Hobby.objects.create(
                    user=form.user,
                    name=name,
               )
               hobby.save()

               return redirect("hobbies:hobby_detail", name=hobby.name)

          return render(request, "hobbies/create_hobby.html", {"form": form})




def hobby_detail_view(request, name):
     if request.method == "GET":
          hobby = get_object_or_404(Hobby, name=name, user=request.user)     # retrieve the Hobby object from the database
          
          delete_url = reverse("hobbies:delete_hobby", args=[hobby.name])
          return render(request, "hobbies/hobby_detail.html", {
               "hobby": hobby,
               "delete_url": delete_url,
          })



def delete_hobby_view(request, name):
     if request.method == "POST":
          hobby = get_object_or_404(Hobby, name=name, user=request.user)    # retrieve the Hobby object from the database

          hobby.delete()
          return redirect("hobbies:hobbies_list")




def hobbies_list_view(request):
     if request.method == "GET":
          user = request.user
          hobbies = user.hobbies.all()
          return render(request, "hobbies/hobbies_list.html", {
               "hobbies": hobbies,
               "user": user,
          })

          
