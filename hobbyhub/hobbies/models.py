from django.db import models

from django.contrib.auth.models import User





class Hobby(models.Model):
     user = models.ForeignKey(
          User, 
          on_delete=models.CASCADE, 
          related_name="hobbies"    # related_name="hobbies" lets us access all of a user's hobbies using user.hobbies
     )

     name = models.CharField(
          unique=True,
          max_length=255,
     )

     date_created = models.DateField(auto_now_add = True)
     # total_time = 


     # database enforces that User does not have duplicates of hobbies
     class Meta:
          constraints = [
               models.UniqueConstraint(
                    fields=['user', 'name'],
                    name='unique_hobby_per_user'
               )
          ]    
