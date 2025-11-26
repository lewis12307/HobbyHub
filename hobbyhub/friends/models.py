from django.db import models
from accounts.models import UserProfile

from django.db.models import F
from django.db.models.functions import Least, Greatest





class FriendRequest(models.Model):
     sender = models.ForeignKey(
          UserProfile, 
          on_delete=models.CASCADE,    # if the UserProfile is deleted, automatically delete the FriendRequest associated with it  
          related_name = "sent_request",
     )

     receiver = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE,     # if the UserProfile is deleted, automatically delete the FriendRequest associated with it  
        related_name = "received_request",
     )

     status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'),
                 ('accepted', 'Accepted'),
                 ('declined', 'Declined')]
     )



     class Meta:
        constraints = [
          # enforce bidirectional uniqueness
          # so only one friend request can exist between two user profiles
          models.UniqueConstraint(
               # make sure any friend request between user profile A and user profile B are treated as the same friend request regardless of who sender and receiver were, by normalizing the order of the two user profiles
               Least(F("sender"), F("receiver")),       # get the smaller of the two UserProfile IDs
               Greatest(F("sender"), F("receiver")),    # get the larger of the two UserProfile IDs
               name="unique_friendship_pair",
          )
        ]








# helper functions for class
        
def send_friend_request(sender, receiver):
     # do nothing if friend request already exists between the two user profiles
     # this prevents duplicate friend requests between profiles
     if FriendRequest.objects.filter(
          models.Q(sender=sender, receiver=receiver) | models.Q(sender=receiver, receiver=sender)
     ).exists():
          return None
     
     else: 
          new_friend_request = FriendRequest.objects.create(
               sender=sender,
               receiver=receiver,
               status='pending',
          )
          new_friend_request.save()


def accept_friend_request(request_id, sender, receiver):
     friend_request = FriendRequest.objects.get(id=request_id, sender=sender, receiver=receiver)
     friend_request.status = 'accepted'
     friend_request.save()


def decline_friend_request(request_id, sender, receiver):
     friend_request = FriendRequest.objects.get(id=request_id, sender=sender, receiver=receiver)
     friend_request.status = 'declined'
     friend_request.save()


def unfriend(user_profile, other_user_profile):
    FriendRequest.objects.get(
        models.Q(sender=user_profile, receiver=other_user_profile) | models.Q(sender=other_user_profile, receiver=user_profile),
        status='accepted',
    ).delete()




def get_pending_friend_requests_received(user_profile):
     pending_friend_requests_received = FriendRequest.objects.filter(
          receiver=user_profile, 
          status='pending',
     )
     return pending_friend_requests_received


def get_pending_friend_requests_sent(user_profile):
     pending_friend_requests_sent = FriendRequest.objects.filter(
          sender=user_profile, 
          status='pending',
     )
     return pending_friend_requests_sent


def get_pending_friends_ids(user_profile):
     pending_friend_requests_sent = get_pending_friend_requests_sent(user_profile)
     sent_pending_friends_ids = list(pending_friend_requests_sent.values_list('receiver', flat=True))

     pending_friend_requests_received = get_pending_friend_requests_received(user_profile)
     received_pending_friends_ids = list(pending_friend_requests_received.values_list('sender', flat=True))

     return sent_pending_friends_ids, received_pending_friends_ids




# get what friend requests were sent by this user profile but were declined 
def get_declined_friend_requests_sent(user_profile):
     declined_friend_requests_sent = FriendRequest.objects.filter(
          sender=user_profile, 
          status='declined',
     )
     return declined_friend_requests_sent

# get the ids of the user profiles that declined the friend requests sent by this user profile
def get_declined_friends_ids(user_profile):
     declined_friends_requests_sent = get_declined_friend_requests_sent(user_profile)
     declined_friends_ids = list(declined_friends_requests_sent.values_list('receiver', flat=True))
     return declined_friends_ids




def get_friend_request(user_profile, other_user_profile):
     # check if a friend request between the two profiles exists
     if FriendRequest.objects.filter(
        models.Q(sender=user_profile, receiver=other_user_profile) | models.Q(sender=other_user_profile, receiver=user_profile),
     ).exists():
     # if a friend request exists, get the FriendRequest object
          friend_request = FriendRequest.objects.get(
               models.Q(sender=user_profile, receiver=other_user_profile) | models.Q(sender=other_user_profile, receiver=user_profile),
          )
          return friend_request
     
     # if a friend request does not exist, return None
     return None 
     

def get_friends(user_profile):
     # get the accepted friend requests sent by the user profile
     accepted_friend_requests_sent = FriendRequest.objects.filter(
          sender=user_profile, 
          status='accepted',
     )
     # get the ids of the user profiles that accepted the friend requests sent by this user profile
     receiver_ids = list(accepted_friend_requests_sent.values_list('receiver', flat=True))      

     # get the accepted friend requests sent to the user
     accepted_friend_requests_received = FriendRequest.objects.filter(
          receiver=user_profile, 
          status='accepted',
     )
     # get the ids of the user profiles that sent friend requests to this user profile which they then accepted
     sender_ids = list(accepted_friend_requests_received.values_list('sender', flat=True))
          
     friends_ids = receiver_ids + sender_ids

     # get all UserProfiles whose id is in friends_ids 
     friends = UserProfile.objects.filter(id__in=friends_ids)
     return friends