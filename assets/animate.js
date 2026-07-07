document.addEventListener('DOMContentLoaded', function () {
  if (typeof gsap === 'undefined') return;

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (typeof ScrollTrigger !== 'undefined') gsap.registerPlugin(ScrollTrigger);

  if (reduceMotion) {
    document.querySelectorAll('[data-reveal],[data-reveal-group]').forEach(function (el) {
      el.style.opacity = 1;
      el.style.transform = 'none';
    });
    return;
  }

  // Section headers + standalone blocks: rise + fade in as they enter view
  gsap.utils.toArray('[data-reveal]').forEach(function (el) {
    gsap.fromTo(el, { opacity: 0, y: 36 }, {
      opacity: 1, y: 0, duration: 0.8, ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 85%' }
    });
  });

  // Card grids / step lists: staggered entrance for direct children
  gsap.utils.toArray('[data-reveal-group]').forEach(function (group) {
    var items = group.children.length ? Array.prototype.slice.call(group.children) : [group];
    gsap.fromTo(items, { opacity: 0, y: 44 }, {
      opacity: 1, y: 0, duration: 0.7, ease: 'power3.out', stagger: 0.12,
      scrollTrigger: { trigger: group, start: 'top 82%' }
    });
  });

  // Hero parallax: swash shapes drift at different speeds on scroll
  gsap.utils.toArray('.swash').forEach(function (el, i) {
    gsap.to(el, {
      y: i === 0 ? 140 : 90,
      ease: 'none',
      scrollTrigger: { trigger: el.closest('header'), start: 'top top', end: 'bottom top', scrub: 1 }
    });
  });

  // Count-up stat numbers
  document.querySelectorAll('.stat .num, .sp-stat .num').forEach(function (el) {
    animateCountUp(el);
  });

  function animateCountUp(el) {
    var textNode = el.childNodes.length ? el.childNodes[0] : null;
    if (!textNode || textNode.nodeType !== 3) return;
    var raw = textNode.nodeValue;
    // Only animate when the whole text node is a clean [prefix][digits/commas] with
    // nothing trailing — ranges like "20-40" or units glued to the number are left
    // fully static rather than risk truncating them mid-animation.
    var match = raw.match(/^([^\d]*)([\d,]+)$/);
    if (!match) return;
    var prefix = match[1], numText = match[2], target = parseInt(numText.replace(/,/g, ''), 10);
    if (isNaN(target)) return;
    var useCommas = numText.indexOf(',') !== -1;
    var counter = { val: 0 };
    gsap.to(counter, {
      val: target, duration: 1.6, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 90%', once: true },
      onUpdate: function () {
        var n = Math.round(counter.val);
        textNode.nodeValue = prefix + (useCommas ? n.toLocaleString('en-US') : n);
      }
    });
  }

  // World map: stagger the dot-matrix in on first scroll into view
  document.querySelectorAll('.world-map-wrap').forEach(function (wrap) {
    var dots = wrap.querySelectorAll('.map-dots circle');
    var hubs = wrap.querySelectorAll('.map-hub');
    var hubDots = wrap.querySelectorAll('.map-hub-dot');
    if (!dots.length) return;
    gsap.set(dots, { transformBox: 'fill-box', transformOrigin: '50% 50%', opacity: 0, scale: 0 });
    gsap.set(hubs, { opacity: 0 });
    gsap.set(hubDots, { transformBox: 'fill-box', transformOrigin: '50% 50%', scale: 0 });
    ScrollTrigger.create({
      trigger: wrap, start: 'top 80%', once: true,
      onEnter: function () {
        gsap.to(dots, {
          opacity: 0.55, scale: 1, duration: 0.4, ease: 'power1.out',
          stagger: { amount: 1.1, from: 'random' }
        });
        gsap.to(hubs, { opacity: 1, duration: 0.3, stagger: 0.15, delay: 0.4, clearProps: 'opacity' });
        gsap.to(hubDots, {
          scale: 1, duration: 0.5, ease: 'back.out(2)', stagger: 0.15, delay: 0.4,
          clearProps: 'scale,transform'
        });
      }
    });
  });
});
