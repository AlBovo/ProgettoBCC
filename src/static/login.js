const imagesNumber = 3;
var previousIndex = 1;

function getRandomImage() {
  var index = Math.floor(Math.random() * imagesNumber) + 1;
  if (index === previousIndex) {
    index = (index) % imagesNumber + 1;
  }
  previousIndex = index;
  return index;
}

function changeBackground() {
  var prevBackgroundImage = document.getElementById(`background-image-${previousIndex}`);
  var newImage = getRandomImage();
  var backgroundImage = document.getElementById(`background-image-${newImage}`);

  prevBackgroundImage.removeAttribute("style");
  prevBackgroundImage.hidden = true;

  backgroundImage.hidden = false;
  backgroundImage.style.opacity = 0;


  setTimeout(function() {
    backgroundImage.style.opacity = 1;
  }, 200); 
}

setInterval(changeBackground, 10000);

modalError = [document.getElementById('buttonClose'), document.getElementById('buttonOk')]

window.closeModal = function(modalId) {
  document.getElementById(modalId).style.display = 'none'
  document.getElementsByTagName('body')[0].classList.remove('overflow-y-hidden')
}

modalError.forEach(function(button) {
  button.addEventListener('click', function() {
    closeModal('modelConfirm')
  })
});