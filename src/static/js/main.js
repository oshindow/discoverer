//Applying roll-over animation on classes using animation.css
$(function(){
      "use strict"; 
    
      $(".primary-btn, .primary-line-btn, .info-box, .post-item").mouseenter(function(event) {
          $(this).addClass("animated pulse");
      });
      
      $(".primary-btn, .primary-line-btn, .info-box, .post-item").on("webkitAnimationEnd mozAnimationEnd oAnimationEnd animationEnd", function(event) {
          $(this).removeClass("animated pulse");
      });
  });

//AOS launch
$(function(){
    "use strict"; 
    AOS.init();
});
                  
//Header Scroll
const debounce = (fn) => {
  let frame;
  return (...params) => {
    if (frame) { 
      cancelAnimationFrame(frame);
    }
    frame = requestAnimationFrame(() => {
      fn(...params);
    });
  } 
};
const storeScroll = () => {
  document.documentElement.dataset.scroll = window.scrollY;
}
document.addEventListener('scroll', debounce(storeScroll), { passive: true });
storeScroll();

//Responsive button menu
$(document).ready(function () {
  $('.first-button').on('click', function () {
    $('.animated-icon').toggleClass('open');
  });
});


//Slick Slider
$(document).ready(function(){
    $('.promo-slider').slick({
      dots: true,
      infinite: true,
      arrows: false,
      centerMode: true,
      autoplay: true,
      autoplaySpeed: 2000,
      slidesToShow: 3,
      slidesToScroll: 2,
      
      responsive: [
          {
          breakpoint: 1280,
          settings: {
            arrows: false,
            centerMode: true,
            slidesToShow: 3
          }
        },
        {
          breakpoint: 980,
          settings: {
            arrows: false,
            centerMode: true,
            slidesToShow: 2
          }
        },
        {
          breakpoint: 768,
          settings: {
            arrows: false,
            centerMode: true,
            slidesToShow: 1
          }
        }
      ]
    });
    AOS.refresh();
});


