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



     # check if user already has a hobby with this name,
     def clean_name(self):
          name = self.cleaned_data.get("name")
          user = getattr(self, "user", None)
          if Hobby.objects.filter(user=user, name__iexact=name).exists():
               raise forms.ValidationError("Hmm… it looks like you already have a hobby with that name. Try a different one.")
          return name




class SortHobbiesForm(forms.Form):
     filter = forms.ChoiceField(choices=["Most Recent", "Creation Date", "Name", "Time Spent"])