from django.db import models
from accounts.models import UserProfile




class EncouragementNote(models.Model):
     sender = models.ForeignKey(
          UserProfile, 
          on_delete=models.CASCADE,    # if the sender’s UserProfile is deleted, all encouragement notes they sent will also be deleted automatically
          related_name="sent_encouragement")
     
     receiver = models.ForeignKey(
          UserProfile, 
          on_delete=models.CASCADE,      # if the receiver's UserProfile is deleted, all encouragement notes they received will also be deleted automatically
          related_name="received_encouragement")
     
     message = models.TextField(max_length=500)

     sent_at = models.DateTimeField(auto_now_add=True)

     seen = models.BooleanField(default=False)
