document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('open');
    });
  }
  var dd = document.querySelector('.nav-dd');
  if (dd) {
    var ddLabel = dd.querySelector('span');
    ddLabel.addEventListener('click', function (e) {
      if (window.matchMedia('(max-width: 760px)').matches) {
        e.preventDefault();
        dd.classList.toggle('open');
      }
    });
  }
});
