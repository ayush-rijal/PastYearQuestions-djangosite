// scripts.js

document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".card");

  cards.forEach((card) => {
    card.addEventListener("mouseover", function () {
      card.querySelector(".card-img-holder img").style.transform = "scale(1.1)";
    });

    card.addEventListener("mouseout", function () {
      card.querySelector(".card-img-holder img").style.transform = "scale(1)";
    });
  });
});
