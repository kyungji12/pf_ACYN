var slideIndex = 0;
showSlides();

function showSlides(){
    var slidesName = document.getElementsByClassName("banner-img");
    var slidesLength = slidesName.length

    for (var i = 0; i < slidesLength; i++) {
        slidesName[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slidesLength) {
        slideIndex = 1
    }
    slidesName[slideIndex-1].style.display = "inline-block";
    setTimeout(showSlides, 2500); // Change images every 2 sec
}

