function openDialog(dialog_id) {
     dialog = document.getElementById(dialog_id)
     dialog.showModal();
}

function closeDialog(dialog_id, form_id) {
     dialog = document.getElementById(dialog_id)
     dialog.close();
     
     const form = document.getElementById(form_id);
     if (form) {
          // reset the form
          form.reset();

          // remove Django error lists
          const errors = form.querySelectorAll('.errorlist');
          errors.forEach(e => e.remove());
     }
}