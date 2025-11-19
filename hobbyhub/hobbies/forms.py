from django import forms

from .models import Hobby






class CreateHobbyForm(forms.Form):
     name = forms.CharField(
          label="Name",
          help_text="Give your new hobby a name.",
          max_length=255,
          strip=True,
          required=True,
          error_messages={
             "required": "Oops... It looks like the name is blank. Please provide one so you can keep track of your new Hobby.",
          }
     )


     def clean_name(self):
          name = self.cleaned_data.get("name")
          user_profile = getattr(self, "user_profile", None)    # get the UserProfile that is attached to the form

          # check if user already has a hobby with the provided name (case insensitive)
          # if they do, raise ValidationError and tell user
          if Hobby.objects.filter(user_profile=user_profile, name__iexact=name).exists():
               raise forms.ValidationError("Hmm… it looks like you already have a hobby with that name. Try a different one.")
          return name








class SortHobbiesForm(forms.Form):     
     sort_choice = forms.ChoiceField(
          label="Sort",
          choices=[
               ("recent_activity", "Recent Activity"),
               ("name", "Name (A–Z)"),
               ("start_date", "Start Date"),
               ("time_spent", "Time Spent"),
               ("number_of_sessions", "Number of Sessions")
          ],
          widget=forms.Select(
               attrs={'onchange': 'this.form.submit();'}     # Automatically submit the form when the user changes the selection
          ),      
          required=False,
    )
     
     order = forms.ChoiceField(
          label="Order",
          choices=[
               ("asc", "Ascending"),
               ("desc", "Descending"),
          ],
           widget=forms.Select(
               attrs={'onchange': 'this.form.submit();'}     # Automatically submit the form when the user changes the selection
          ),    
          required=False,
    )