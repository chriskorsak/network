document.addEventListener("DOMContentLoaded", function() {
  // add click event to all post edit buttons
  let buttons = document.querySelectorAll('button');
  buttons.forEach(function(button) {
    button.addEventListener('click', function() {
      editPost(button);
    });
  });
  // add click event to all like heart icons
  let likeIcons = document.querySelectorAll('.svg-logged-in');
  likeIcons.forEach(function(likeIcon) {
    likeIcon.addEventListener('click', function() {
      likePost(likeIcon);
    });
  });
});

function editPost(button) {
  //disable edit button to prevent multiple clicks
  button.disabled = true;

  // create buttons for canceling or saving post edit
  let save = document.createElement('button');
  save.innerText = 'save';
  save.classList.add('btn', 'btn-outline-dark', 'btn-sm');
  let cancel = document.createElement('button');
  cancel.innerText = 'cancel';
  cancel.classList.add('btn', 'btn-outline-dark', 'btn-sm', 'nudge-button');


  // assign post text element to postText variable
  postText = button.nextElementSibling;

  //get parent element of button
  let post = button.parentNode;

  //insert cancel and save butttons before post text
  postText.insertAdjacentElement('beforebegin', cancel);
  postText.insertAdjacentElement('beforebegin', save);

  //create textarea and insert/replace postText data
  let editPostText = document.createElement('textarea');
  editPostText.innerText = postText.innerText;
  editPostText.classList.add('form-control', 'post-text');
  post.replaceChild(editPostText, postText);

  // cancel edit: add click event to cancel, switch back to paragraph post text
  // remove cancel and save buttons, enable edit button again.
  cancel.addEventListener('click', function() {
    post.replaceChild(postText, editPostText);
    save.remove();
    cancel.remove();

    button.disabled = false;
  });

  // save edit
  save.addEventListener('click', function() {
    //get parent div post id (the entire post container element)
    let postId = post.id;
    //get updated post text after user edits
    let editedPostTextVal = editPostText.value;

    // fetch(`/edit-post/${postId}`)
    fetch(`/edit-post/${postId}`, {
      method: 'POST',
      body: JSON.stringify({
          postText: editedPostTextVal,
          postId: postId
      })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .then(postText.innerText = editedPostTextVal)
    .then(post.replaceChild(postText, editPostText))

    //remove cancel/save buttons and enable edit button
    save.remove();
    cancel.remove();
    button.disabled = false;
  });
}

function likePost(likeIcon) {
  //turn icon red or black when clicked
  likeIcon.classList.toggle('liked');

  //get parent div (the entire post container element)
  let divParent = likeIcon.parentElement.parentElement;
  let postId = divParent.id;

  //update post likes using fetch api
  fetch(`/like-post/${postId}`, {
    method: 'POST',
    body: JSON.stringify({
        postId: postId
    })
  })
  .then(response => response.json())
  .then(data => {
    // get number of likes count from page to be updated
    let postLikesCount = document.querySelector(`#likes-post-${postId}`);
    let updatedLikeCount = data.updatedLikeCount;
    postLikesCount.innerText = updatedLikeCount;
  })
}