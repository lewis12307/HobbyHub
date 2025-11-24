function openDialog(dialog_id) {
     dialog = document.getElementById(dialog_id)
     dialog.showModal();
}

function closeDialog(dialog_id, form_id) {
     dialog = document.getElementById(dialog_id)
     dialog.close();
}