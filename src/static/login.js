var previousIndex = -1;

function getRandomImage() {
  var index = Math.floor(Math.random() * images.length);
  while (index === previousIndex) {
    index = Math.floor(Math.random() * images.length);
  }

  previousIndex = index;
  return index+1;
}

function changeBackground() {
  var newImage = getRandomImage();
  var backgroundImage = document.getElementById('background-image${newImage}');

  backgroundImage.style.opacity = 0;

  setTimeout(function() {
    backgroundImage.src = newImage;
    backgroundImage.style.opacity = 1;
  }, 500); 
}

setInterval(changeBackground, 10000);