from django.shortcuts import render


def dashboard_view(request):
     if request.method == "GET":
          return render(request, "dashboard.html")