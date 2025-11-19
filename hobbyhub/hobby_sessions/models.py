from django.db import models

from accounts.models import UserProfile
from hobbies.models import Hobby

from datetime import datetime, timedelta
from django.db.models import Q






class Session(models.Model):
     user_profile = models.ForeignKey(
          UserProfile, 
          on_delete=models.CASCADE,    # if the UserProfile is deleted, automatically delete all Sessions that belong to it
     )

     hobby = models.ForeignKey(
        Hobby,
        on_delete=models.CASCADE,    # if the Hobby is deleted, automatically delete all Sessions associated with it 
        related_name='sessions',     # enables reverse lookup: hobby.sessions returns all sessions for given Hobby object
    )




     date = models.DateField()

     start_time = models.TimeField()
     end_time = models.TimeField()
     @property
     def duration(self):
          # To calculate a duration, Python needs datetime objects
          # So, combine date and start_time into one datetime object and combine date and end_time into another datetime object
          start_dt = datetime.combine(self.date, self.start_time)
          end_dt = datetime.combine(self.date, self.end_time)

          # calculate the total duration of the session
          # returns the duration as a timedelta (HH:MM:SS)
          return end_dt - start_dt




     description = models.TextField(
          blank=True, 
          null=True)

     upload = models.ImageField(
        upload_to='session_pictures/', 
        blank=True, 
        null=True)   
     
     friend_visibiilty = models.BooleanField(default=True)



    
     class Meta:
        constraints = [
            
             # enforce at the database level that at least either description or upload must be provided
            models.CheckConstraint(
               name="require_description_or_upload",
               check=(
                    Q(description__isnull=False) | Q(upload__isnull=False)
               ),
            )
        ]