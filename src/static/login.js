var previousIndex = 1;

function getRandomImage() {
  var index = Math.floor(Math.random() * images.length);
  while (index === previousIndex) {
    index = Math.floor(Math.random() * images.length);
  }
  index++;
  previousIndex = index;
  return index;
}

function changeBackground() {
  var newImage = getRandomImage();
  var prevBackgroundImage = document.getElementById('background-image${previousIndex}');
  var backgroundImage = document.getElementById('background-image${newImage}');

  prevBackgroundImage.hidden = true;
  backgroundImage.hidden = false;
  backgroundImage.style.opacity = 0;

  setTimeout(function() {
    backgroundImage.src = newImage;
    backgroundImage.style.opacity = 1;
  }, 500); 
}

setInterval(changeBackground, 10000);