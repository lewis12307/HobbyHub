from django.db import models
from accounts.models import UserProfile

from django.db.models import F
from django.db.models.functions import Least, Greatest





class FriendRequest(models.Model):
     sender = models.ForeignKey(
          UserProfile, 
          on_delete=models.CASCADE,    # if the UserProfile is deleted, automatically delete the FriendRequest associated with it     
          related_name='sent_request',
     )

     receiver = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE,     # if the UserProfile is deleted, automatically delete the FriendRequest associated with it  
        related_name='received_request',    
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
     # do nothing if friend request already exists between the two profiles
     # prevents duplicate requests between profiles
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
     pending_friends_requests_sent = get_pending_friend_requests_sent(user_profile)
     pending_friends_ids = list(pending_friends_requests_sent.values_list('receiver', flat=True))
     return pending_friends_ids


def get_friend_status(user_profile, other_user_profile):
     # check if a friend request between the two profiles exists
     if FriendRequest.objects.filter(
        models.Q(sender=user_profile, receiver=other_user_profile) | models.Q(sender=other_user_profile, receiver=user_profile),
     ).exists():
          friend_request = FriendRequest.objects.get(
               models.Q(sender=user_profile, receiver=other_user_profile) | models.Q(sender=other_user_profile, receiver=user_profile),
          )
          status = friend_request.status
          return status
     else:
          return None 
     

def get_friends(user_profile):
     # get accepted friend requests sent by the user
     accepted_requests_sent = FriendRequest.objects.filter(
          sender=user_profile, 
          status='accepted',
     )
     # get the ids of the recipients of accepted friend requests sent by the user
     receiver_ids = list(accepted_requests_sent.values_list('receiver', flat=True))      

     # get accepted friend requests sent to the user
     accepted_requests_received = FriendRequest.objects.filter(
          receiver=user_profile, 
          status='accepted',
     )
     # get the ids of the senders of accepted friend requests to the user
     sender_ids = list(accepted_requests_received.values_list('sender', flat=True))
          
     friend_ids = receiver_ids + sender_ids
     # get all UserProfiles whose id is in friend_ids 
     friends = UserProfile.objects.filter(id__in=friend_ids)
     return friends


def unfriend(user_profile, other_user_profile):
    FriendRequest.objects.get(
        models.Q(sender=user_profile, receiver=other_user_profile) | models.Q(sender=other_user_profile, receiver=user_profile),
        status='accepted',
    ).delete()