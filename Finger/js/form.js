const slidePage = document.querySelector(".slidepage");
const firstNextBtn = document.querySelector(".nextBtn");
const prevBtnSec = document.querySelector(".Prev-1");
const nextBtnSec = document.querySelector(".Next-1");
const prevBtnThird = document.querySelector(".Prev-2");
const nextBtnThird = document.querySelector(".Next-2");
const prevBtnFourth = document.querySelector(".Prev-3");
const submitBtn = document.querySelector(".Submit");
const progressText = document.querySelectorAll(".step p");
const progressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");
const content = document.querySelector(".container");
let max = 4;
let current = 1;

firstNextBtn.addEventListener("click", function () {
    slidePage.style.marginLeft = "-25%";
    content.style.height="400px";
    bullet[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    current += 1;
});
nextBtnSec.addEventListener("click", function () {
    slidePage.style.marginLeft = "-50%";
    content.style.height="500px";
    bullet[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    current += 1;
});
nextBtnThird.addEventListener("click", function () {
    slidePage.style.marginLeft = "-75%";
    content.style.height="500px";
    bullet[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    current += 1;
});


prevBtnSec.addEventListener("click", function () {
    slidePage.style.marginLeft = "0%";
});
prevBtnThird.addEventListener("click", function () {
    slidePage.style.marginLeft = "-25%";
});
prevBtnFourth.addEventListener("click", function () {
    slidePage.style.marginLeft = "-50%";
});

submitBtn.addEventListener("click", function () {
    bullet[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    current += 1;
    setTimeout(function () {
        alert("Vita!!!");
        location.reload();
    }, 800)
});

prevBtnSec.addEventListener("click", function () {
    content.style.height="1040px";
    slidePage.style.marginLeft = "0%";
    bullet[current - 2].classList.remove("active");
    progressText[current - 2].classList.remove("active");
    progressCheck[current - 2].classList.remove("active");
    current -= 1;
});
prevBtnThird.addEventListener("click", function () {
    slidePage.style.marginLeft = "-25%";
    content.style.height="400px";
    bullet[current - 2].classList.remove("active");
    progressText[current - 2].classList.remove("active");
    progressCheck[current - 2].classList.remove("active");
    current -= 1;
});
prevBtnFourth.addEventListener("click", function () {
    slidePage.style.marginLeft = "-50%";
    content.style.height="500px";
    bullet[current - 2].classList.remove("active");
    progressText[current - 2].classList.remove("active");
    progressCheck[current - 2].classList.remove("active");
    current -= 1;
});