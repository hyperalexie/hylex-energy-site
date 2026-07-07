document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.world-map-wrap').forEach(function (wrap) {
    var svg = wrap.querySelector('.world-map');
    var tooltip = wrap.querySelector('.map-tooltip');
    if (!svg || !tooltip) return;
    var nameEl = tooltip.querySelector('.map-tooltip-name');
    var roleEl = tooltip.querySelector('.map-tooltip-role');
    var detailEl = tooltip.querySelector('.map-tooltip-detail');
    var activeHub = null;

    function showHub(hub) {
      var rect = hub.querySelector('.map-hub-dot').getBoundingClientRect();
      var wrapRect = wrap.getBoundingClientRect();
      nameEl.textContent = hub.dataset.name;
      roleEl.textContent = hub.dataset.role;
      detailEl.innerHTML = '';
      hub.dataset.detail.split('•').forEach(function (point) {
        point = point.trim();
        if (!point) return;
        var li = document.createElement('li');
        li.textContent = point;
        detailEl.appendChild(li);
      });
      tooltip.style.left = (rect.left + rect.width / 2 - wrapRect.left) + 'px';
      tooltip.style.top = (rect.top - wrapRect.top) + 'px';
      tooltip.classList.add('visible');
      hub.classList.add('active');
    }

    function hideHub(hub) {
      hub.classList.remove('active');
      tooltip.classList.remove('visible');
    }

    svg.querySelectorAll('.map-hub').forEach(function (hub) {
      hub.addEventListener('mouseenter', function () { showHub(hub); });
      hub.addEventListener('mouseleave', function () { hideHub(hub); });
      hub.addEventListener('focus', function () { showHub(hub); });
      hub.addEventListener('blur', function () { hideHub(hub); });
      hub.addEventListener('click', function (e) {
        e.preventDefault();
        if (activeHub === hub) {
          hideHub(hub);
          activeHub = null;
        } else {
          if (activeHub) hideHub(activeHub);
          showHub(hub);
          activeHub = hub;
        }
      });
    });

    document.addEventListener('click', function (e) {
      if (activeHub && !wrap.contains(e.target)) {
        hideHub(activeHub);
        activeHub = null;
      }
    });
  });
});
