/* Sublime Personnel — prototype behaviour: header state, drawer, dropdown, reveal */
(function () {
  "use strict";
  var hdr = document.querySelector(".hdr");
  function onScroll() { if (hdr) hdr.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  var burger = document.querySelector(".burger");
  if (burger) {
    burger.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      document.documentElement.style.overflow = open ? "hidden" : "";
    });
    document.querySelectorAll(".drawer a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("menu-open");
        burger.setAttribute("aria-expanded", "false");
        document.documentElement.style.overflow = "";
      });
    });
  }

  document.querySelectorAll(".has-menu").forEach(function (w) {
    var btn = w.querySelector("button"); if (!btn) return;
    function close() { w.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var o = w.classList.toggle("open"); btn.setAttribute("aria-expanded", o ? "true" : "false");
    });
    w.addEventListener("mouseenter", function () { w.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    w.addEventListener("mouseleave", close);
    document.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  });

  var rv = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window && rv.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -7% 0px", threshold: .05 });
    rv.forEach(function (el, i) { el.style.transitionDelay = (Math.min(i % 4, 3) * 75) + "ms"; io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add("in"); }); }

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
