from accounts.models import UserProfile
from friends.models import get_friends


from django import forms
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea



class EncouragementNoteForm(forms.Form):
     recipient = forms.CharField(
          label="To", 
          widget=forms.TextInput(attrs={
               "autocomplete": "off",
          }),
          help_text="Enter the username of the friend you would like to send a note to.", 
          max_length=255, 
          strip=True, 
          required=True, 
     )

     message = forms.CharField(
          label="Message", 
          widget=EmojiPickerTextarea(attrs={"rows": 3}),
          strip=True, 
          required=True, 
          error_messages={
               "required": "Please don’t leave this blank :(. Your friend would love to hear something kind from you.",
          },
     )




     def clean_recipient(self):
          recipient_username = self.cleaned_data.get("recipient")

          # check if the provided username exists
          try:
               recipient_profile = UserProfile.objects.get(user__username=recipient_username)
          except UserProfile.DoesNotExist:
               raise forms.ValidationError("Hmm.. there is no profile with that username.")

          # check if the sender and intended recipient are friends
          sender_current_friends = get_friends(self.sender_profile)  
          if recipient_profile not in sender_current_friends:
               raise forms.ValidationError("Hmm... you do not have a friend with that username. You can only send notes to your friends.")

          return recipient_username

