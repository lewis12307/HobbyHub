from django import forms
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

from datetime import date, datetime
from django.utils import timezone

from django.core.validators import validate_image_file_extension





class CreateSessionForm(forms.Form):
     date = forms.DateField(
          label="Date",
          widget=forms.DateInput(attrs={'type': 'date'}),
          required=True, 
     )

     start_time = forms.TimeField(
          label="Start Time", 
          widget=forms.TimeInput(attrs={'type': 'time'}), 
          required=True, 
     )
     end_time = forms.TimeField(
          label="End Time", 
          widget=forms.TimeInput(attrs={'type': 'time'}), 
          required=True, 
     )

     description = forms.CharField(
          label="Little blurb", 
          help_text="Write a little note about your session.",
          widget=EmojiPickerTextarea(attrs={"rows": 3}),
          required=False, 
          strip=True,
     )

     upload = forms.ImageField(
          label="Session Snapshot", 
          help_text="Add a photo that captures what you did during this session.",
          widget=forms.FileInput(),
          required=False,
          validators=[validate_image_file_extension],
          error_messages={     # override default error messages to be friendlier
               "invalid_extension": "Hmm… that file doesn’t seem to be an image. Please upload a JPG or PNG.",
               "invalid_image": "Hmm… that file doesn’t look like an image I can read. Please upload a different file.",
          } 
     )

     friend_visibility = forms.BooleanField(
          label="Show to friends?", 
          widget=forms.CheckboxInput(), 
          required=False, 
          initial=True,    # checkbox starts checked
     )









     # check that the provided date is not in the future
     def clean_date(self):
          today = timezone.localdate()

          date = self.cleaned_data.get("date")
          if date and date > today:
               raise forms.ValidationError(
                    "Hmm... that date hasn’t happened yet. Please pick a date that’s in the past or today."
               )
          return date

     


     def clean_description(self):
          description = self.cleaned_data.get("description")

          # if empty or None, let clean() handle the "either description or upload" rule
          if description is None or description=="":
               return description

          # check that description is not just whitespace
          if description.strip() == "":
               raise forms.ValidationError(
                    "Please add a little note that isn’t just empty space."
               )
          return description
   

     def clean(self):
          cleaned_data = super().clean()

          # require either upload or description
          description = cleaned_data.get("description")
          upload = cleaned_data.get("upload")
          if not description and not upload:
               self.add_error(
                    "description",
                    "Please add a short note or a photo to remember this session."
               )
               self.add_error(
                    "upload",
                    "Please add a short note or a photo to remember this session."
               )




          start_time = cleaned_data.get("start_time")
          end_time = cleaned_data.get("end_time")

          if not start_time or not end_time:
               return cleaned_data

          # check that the end time is after the start time
          if start_time and end_time and end_time <= start_time:
               self.add_error(
                    "start_time",
                    "Oops.. these times don’t quite line up. Please make sure the end time is later than the start time."
               )
               self.add_error(
                    "end_time",
                    "Oops.. these times don’t quite line up. Please make sure the end time is later than the start time."
               )
          
          


          today = timezone.localdate()
          now = timezone.localtime()
          date = self.cleaned_data.get("date")
          # if provided date is in past, do nothing
          if date and date < today:      
               pass
          # if provided date is today or in past, check that provided start and end times are not in future, regardless of provided date
          else:                
               # checking whether a time is in the future requires the full date and time together,
               # so we combine the user's date and time inputs into real datetime objects before validating
               session_start = timezone.make_aware(
                    datetime.combine(today, start_time)
               )
               session_end = timezone.make_aware(
               datetime.combine(today, end_time)
               )

               # check that start time is not in the future
               if session_start > now:
                    self.add_error(
                         "start_time",
                         "Hmm... that time hasn’t happened yet. Please pick a time that’s in the past or right now."
                    )
          
               # check that end time is not in the future
               if session_end > now:
                    self.add_error(
                         "end_time",
                         "Hmm... that time hasn’t happened yet. Please pick a time that’s in the past or right now."
                    )

          return cleaned_data

     

     




class EditSessionForm(CreateSessionForm):
     pass

     # custom validation here if needed 