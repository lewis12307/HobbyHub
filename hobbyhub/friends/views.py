from accounts.models import UserProfile
from friends.models import FriendRequest, send_friend_request, accept_friend_request, decline_friend_request, get_pending_friend_requests_received, get_pending_friends_ids, get_declined_friends_ids, get_friends, unfriend


from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse






@login_required
def friends_view(request):
     current_user = request.user
     current_user_profile = current_user.userprofile

     pending_friend_requests = get_pending_friend_requests_received(current_user_profile)

     current_friends = get_friends(current_user_profile)

     return render(request, "friends/friends.html", {
          "pending_friend_requests": pending_friend_requests,
          "current_friends": current_friends,
     })


@login_required
def search_friend_view(request):
     current_user = request.user
     current_user_profile = current_user.userprofile

     current_friends = get_friends(current_user_profile)
     current_friends_ids = current_friends.values_list('id', flat=True)
     sent_pending_friends_ids = get_pending_friends_ids(current_user_profile)[0]
     received_pending_friends_ids = get_pending_friends_ids(current_user_profile)[1]
     declined_friend_ids = get_declined_friends_ids(current_user_profile)

     # get the user's search text from the URL
     # (defaults to an empty string if nothing was typed)
     search_term = request.GET.get("q", "")

     # query all UserProfile objects where the related User's username contains the search term
     results = UserProfile.objects.filter(
          user__username__icontains=search_term
     ).exclude(       # exclude current logged-in user from search results
          user=current_user  
     ).exclude(       # exclude user's current friends from search results
          id__in=current_friends_ids
     ).exclude(       # exclude user profiles that have declined a friend request from the current user profile from the search results
          id__in=declined_friend_ids
     ).exclude(       # exclude user profiles that have already sent the current user profile a friend request from the search results, to prevent duplicate friend requests for the same user prorifle pair
          id__in=received_pending_friends_ids
     )
     
     return render(request, "friends/add_friend.html", {
          "search_term": search_term,
          "results": results, 
          "sent_pending_friends_ids": sent_pending_friends_ids,
     })
     

@login_required
def add_friend_view(request):
     if request.method == "POST":
          friend_username = request.POST.get('friend_username')
          # get the UserProfile with that username
          friend_user_profile = UserProfile.objects.get(user__username=friend_username)
          
          send_friend_request(
               sender=request.user.userprofile, 
               receiver=friend_user_profile,
          )

          old_search = request.POST.get('old_search')
          friend_profile_url = reverse('accounts:profile', args=[friend_user_profile.user.username])
          return redirect(f"{friend_profile_url}?q={old_search}")

     else:     # if request method is GET or anything else     
          return render(request, "friends/add_friend.html")


@login_required
def respond_friend_request_view(request):
     if request.method == "POST":
          friend_request_id = request.POST.get("friend_request_id") 

          receiver = request.user.userprofile

          sender_username = request.POST.get("friend_username")   
          sender = UserProfile.objects.get(user__username=sender_username)
          
          friend_request_response = request.POST.get("friend_request_response")
          if friend_request_response == "accept":
               accept_friend_request(friend_request_id, sender, receiver)
          if friend_request_response == "decline":
               decline_friend_request(friend_request_id, sender, receiver)
          
          return redirect("friends:friends")
     

@login_required
def remove_friend_view(request):
     if request.method == "POST":
          current_user = request.user
          current_user_profile = current_user.userprofile

          friend_username = request.POST.get('friend_username')
          friend_user_profile = UserProfile.objects.get(user__username=friend_username)

          unfriend(current_user_profile, friend_user_profile)
          
          return redirect('friends:friends')