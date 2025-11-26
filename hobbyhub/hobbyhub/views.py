from django.contrib.auth.decorators import login_required

from django.shortcuts import render





@login_required
def dashboard_view(request):
     if request.method == "GET":
          user = request.user
          profile = user.userprofile
          
          return render(request, "dashboard.html", {
                    "user": user,
                    "profile": profile,
          })