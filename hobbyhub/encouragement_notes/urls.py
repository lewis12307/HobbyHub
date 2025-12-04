from django.urls import path
from .views import send_encouragement_view, see_encouragement_view



app_name = "encouragement_notes"

urlpatterns = [
     path("friends/kudos/send/", send_encouragement_view, name="send_encouragement"),
     path("kudos/", see_encouragement_view, name="view_encouragement"),
]