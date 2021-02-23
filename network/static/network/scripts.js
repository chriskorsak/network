document.addEventListener("DOMContentLoaded", function() {
  let buttons = document.querySelectorAll('button');
  buttons.forEach(function(button) {
    button.addEventListener('click', function() {
      editPost(button);
    });
  });
});

function editPost(button) {
  //disable edit button to prevent multiple clicks
  button.disabled = true;

  // create buttons for canceling or saving post edit
  let save = document.createElement('button');
  save.innerText = 'save';
  let cancel = document.createElement('button');
  cancel.innerText = 'cancel';

  // assign post text element to postText variable
  postText = button.nextElementSibling;

  //get parent of button
  let post = button.parentNode;

  //insert cancel and save butttons before post text
  postText.insertAdjacentElement('beforebegin', cancel);
  postText.insertAdjacentElement('beforebegin', save);

  //create textarea and insert/replace postText data
  let editPostText = document.createElement('textarea');
  editPostText.innerText = postText.innerText;
  post.replaceChild(editPostText, postText);

  // cancel edit: add click event to cancel, switch back to paragraph post text
  // remove cancel and save buttons, enable edit button again.
  cancel.addEventListener('click', function() {
    post.replaceChild(postText, editPostText);
    save.remove();
    cancel.remove();

    button.disabled = false;
  });



}