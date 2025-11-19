from django.db import models

from django.contrib.auth.models import User
from accounts.models import UserProfile

from datetime import datetime, timedelta





class Hobby(models.Model):
     user_profile = models.ForeignKey(
          UserProfile, 
          on_delete=models.CASCADE,   # if the UserProfile is deleted, automatically delete all Hobbies associated with that profile
          related_name="hobbies"    # enables reverse lookup: user.hobbies returns all hobbies for given User object
     )

     name = models.CharField(
          unique=True,
          max_length=255,
     )



     date_created = models.DateField(auto_now_add = True)

     @property
     def total_time_spent(self):
          total_time = timedelta()
          all_sessions = self.sessions.all()    # get all sessions that are associated with this Hobby
          # get the duration of each session and add them together to find the total amount of time spent on this Hobby
          for session in all_sessions:
               total_time += session.duration    
          return total_time


     @property
     def number_of_sessions(self):
          number_of_sessions = self.sessions.count()
          return number_of_sessions





     class Meta:
          constraints = [
               # database enforces that a UserProfile has no duplicates of any hobbies, each Hobby name is unique
               models.UniqueConstraint(
                    fields=['user_profile', 'name'],
                    name='unique_hobby_per_user_profile'
               )
          ]    
