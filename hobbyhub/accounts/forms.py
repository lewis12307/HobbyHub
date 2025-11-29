from accounts.models import UserProfile


from django import forms
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

from django.core.validators import RegexValidator, MinLengthValidator, validate_image_file_extension
from accounts.validators import username_validator





class SignUpForm(forms.Form):
     first_name = forms.CharField(
          label="First Name *", 
          widget=forms.TextInput(attrs={
               "autocomplete": "off",
          }),
          help_text="Please enter your first name, using only letters and hyphens.", 
          max_length=255, 
          strip=True, 
          required=True, 
          validators=[RegexValidator(
               regex=r'^[^\W\d_]+(?:-[^\W\d_]+)*$',     # checks name contains only letters from any language and hyphens 
               message="Oops ... It looks like your first name has characters that aren't allowed. Please use letters and hyphens only.",
               code='invalid_first_name'
          )]
     )

     last_name = forms.CharField(
          label="Last Name", 
          widget=forms.TextInput(attrs={
               "autocomplete": "off",
          }),
          help_text="Please enter your last name, using only letters and hyphens.", 
          max_length=255, 
          strip=True, 
          required=False, 
          validators=[RegexValidator(
               regex=r'^[^\W\d_]+(?:-[^\W\d_]+)*$',     # checks name contains only letters from any language and hyphens 
               message="Oops ... It looks like your last name has characters that aren't allowed. Please use letters and hyphens only.",
               code='invalid_last_name'
          )]
     )
     
     username = forms.CharField(
          label="Username *", 
          widget=forms.TextInput(attrs={
               "autocomplete": "off",
          }),
          help_text="Please enter a username, using only letters, numbers, underscores (_), and hyphens (-).", 
          max_length=150, 
          strip=True, 
          required=True, 
          validators=[username_validator]    # checks username contains only Unicode letters, numbers, underscores, hyphens
                                             # see clean_username below for username uniquenes validation
     )   
     

     password = forms.CharField(
          label="Password *", 
          widget=forms.PasswordInput(attrs={
               "autocomplete": "new-password",
          }),
          help_text="Please enter a strong password and make sure it is at least 8 characters long.", 
          max_length=255, 
          strip=True, 
          required=True, 
          validators = [MinLengthValidator(
               limit_value=8, 
               message="Oops ... It looks like your password is too short. Try making it at least 8 characters long.",
          )],
     )    


     bio = forms.CharField(
          label="Bio", 
          widget=EmojiPickerTextarea(attrs={"rows": 3}),
          help_text="Write a short bio to share a little about yourself.", 
          required=False, 
          empty_value=None,
     )
     

     profile_picture = forms.ImageField(
          label="Profile Picture", 
          widget=forms.FileInput(),
          help_text="Upload a little picture to display on your profile.", 
          required=False,
          validators=[validate_image_file_extension],
          error_messages={     # override default error messages to be friendlier
               "invalid_extension": "Hmm… that file doesn’t seem to be an image. Please upload a JPG or PNG.",
               "invalid_image": "Hmm… that file doesn’t seem to be an image. Please upload a JPG or PNG.",
          }
     )



     # checks whether the username is already taken or not
     def clean_username(self):
          username = self.cleaned_data.get("username")
          if UserProfile.objects.filter(user__username=username).exists():
               raise forms.ValidationError(
                    "Oops… That username is already taken. Try to think of a unique one that feels like you.",
                    code="unique_username"
               )
          return username
     
     








class LoginForm(forms.Form):
     username = forms.CharField(
          label="Username",  
          widget=forms.TextInput(attrs={
               "autocomplete": "off",
          }),
          max_length=150, 
          strip=True, 
          required=True,
     )   

     password = forms.CharField(
          label="Password", 
          widget=forms.PasswordInput(attrs={
               "autocomplete": "new-password",
          }),
          max_length=255, 
          strip=True, 
          required=True,
     )



     # check that provided username exists and it is tied to an account in database 
     # if not, notify user
     def clean_username(self):
          username = self.cleaned_data.get("username")
          if not UserProfile.objects.filter(user__username=username).exists():
               raise forms.ValidationError(
                    "Hmm… We couldn’t find anyone with that username. Want to try again?"
               )
          return username








class EditProfileForm(SignUpForm):
     password = None       # user will not be able to edit password in this form
    


     # checks whether the username is already taken or not
     # not including user's current username
     def clean_username(self):
          current_user = getattr(self, "user", None)
          current_username = current_user.username
          new_username = self.cleaned_data.get("username")


          # if new username is the same as current username, 
          # do not raise a validation error and return the new username
          if new_username == current_username:
               return new_username
          
          # othewise, check that the new username is unique 
          if UserProfile.objects.filter(user__username=new_username).exists():
               raise forms.ValidationError(
                    "Oops… That username is already taken. Try to think of a unique one that feels like you.",
                    code="unique_username"
               )
          return new_username



