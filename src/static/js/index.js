document.addEventListener('DOMContentLoaded', function () {
    var i = 0;
    var txt = "UN PROGETTO DI"; /* The text */
    var speed = 100; /* The speed/duration of the effect in milliseconds */
    var f = false;

    function typeWriter() {
        if (i < txt.length) {
            document.getElementById("progetto").innerHTML += txt.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
        else {
            return;
        }
    }
    typeWriter();
    setTimeout(() => {
        var text = document.getElementById("progetto");
        text.innerHTML = "";
        text.classList.remove(...["text-5xl", "sm:text-6xl", "md:text-7xl", "lg:text-8xl"]);
        text.classList.add(...["text-7xl", "sm:text-8xl", "md:text-9xl", "lg:text-10xl"]);
        i = 0;
        txt = "BLAISONE"; /* The text */
        typeWriter();
    }, 2000);
});
