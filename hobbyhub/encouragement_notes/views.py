from encouragement_notes.models import EncouragementNote
from accounts.models import UserProfile

from encouragement_notes.forms import EncouragementNoteForm
from django.contrib import messages

from django.shortcuts import render
from django.shortcuts import redirect








def send_encouragement_view(request):
     selected_page = "friends"
     if request.method == "POST":
          # create a form instance and fill it with the data the user submitted
          encouragement_note_form = EncouragementNoteForm(request.POST)

          # attach the sender's UserProfile to the form to help with form input validation
          sender = request.user.userprofile
          encouragement_note_form.sender_profile = sender


          # validate and process form input
          if encouragement_note_form.is_valid():
               cleaned_input = encouragement_note_form.cleaned_data
               recipient_username = cleaned_input["recipient"]
               receiver = UserProfile.objects.get(user__username=recipient_username)
               message = cleaned_input["message"]

               # create new EncouragementNote instance
               new_encouragement_note = EncouragementNote.objects.create(
                    sender=sender, 
                    receiver=receiver, 
                    message=message, 
               )
               # persist EncouragementNote to database
               new_encouragement_note.save()  

               messages.success(request, f"Kudos has been sent to @{receiver.user.username}! They will love it!")
               return redirect('accounts:profile', recipient_username)

          # if input is invalid, notify user and show form again with errors
          return render(request, "encouragement_notes/write_encouragement_note.html", {
               "encouragement_note_form": encouragement_note_form,
               "recipient_username": recipient_username,
               "selected_page": selected_page,
          })

     else:
          # get the username of the intended recipient, which was passed as a parameter in the URL
          # use this to autofill the receiver ("To") field of the form
          initial_data = {}
          recipient_username = request.GET.get("to", "")
          if recipient_username:
               initial_data = {"recipient": recipient_username} 

          encouragement_note_form = EncouragementNoteForm(initial=initial_data)

          # render the template and show the form so the user can write a note of encouragement for their friend
          return render(request, "encouragement_notes/write_encouragement_note.html", {
               "encouragement_note_form": encouragement_note_form,
               "recipient_username": recipient_username,
               "selected_page": selected_page,
          })






def see_encouragement_view(request):
     current_user = request.user
     current_user_profile = current_user.userprofile

     # get all the encouragement notes that have been sent to the given user profile 
     received_notes = current_user_profile.received_encouragement.all()
     received_notes_sorted = received_notes.order_by("-sent_at")
     
     # get the encouragement notes that have already been seen 
     old_notes = list(received_notes_sorted.filter(seen=True))
     # get the encouragement notes that have not been seen yet
     new_notes = list(received_notes_sorted.filter(seen=False))

     # update all the unseen encouragement notes to be seen now
     unseen_notes = received_notes_sorted.filter(seen=False)
     unseen_notes.update(seen=True)

     selected_page = "encouragement_notes"
     return render(request, "encouragement_notes/received_encouragement_notes.html", {
        "received_notes": received_notes,
        "new_notes": new_notes,
        "old_notes": old_notes,
        "selected_page": selected_page,
     })









