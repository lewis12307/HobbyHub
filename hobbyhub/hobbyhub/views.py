from friends.models import get_friends
from hobby_sessions.models import Session


from django.contrib.auth.decorators import login_required

from django.shortcuts import render





@login_required
def dashboard_view(request):
     current_user = request.user
     current_user_profile = current_user.userprofile

     friends = get_friends(current_user_profile)
     recent_friend_sessions = (
          Session.objects
          .filter(
               user_profile__in=friends, 
               friend_visibility=True
          ).order_by("-date", "-end_time")
          [:10]   # limit to 10 most recent
     )

     all_encouragement_notes = current_user_profile.received_encouragement.all()
     all_encouragement_notes_sorted = all_encouragement_notes.order_by("-sent_at")
     new_encouragement_notes = list(all_encouragement_notes_sorted.filter(seen=False))
          

     selected = "dashboard"
     return render(request, "dashboard.html", {
          "recent_friend_sessions": recent_friend_sessions,
          "new_encouragement_notes": new_encouragement_notes,
          "selected_page": selected,
     })