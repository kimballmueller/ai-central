/* =========================================================
   Sublime Personnel — site behaviour
   Header state · mobile drawer · dropdowns · reveal · forms
   ========================================================= */
(function () {
  "use strict";

  var SITE = {
    /* --- PASTE the form endpoint here to go live ---------------------
       Accepts any URL that takes a JSON POST: a GoHighLevel inbound
       webhook, a Zapier/Make catch hook, or a Formspree endpoint.
       While this is empty, submissions fall back to a mailto: draft so
       the form is never a dead end on the staging link.               */
    FORM_ENDPOINT: "",
    FALLBACK_EMAIL: "pete@sublimepersonnel.com",
    PHONE: "713-396-0944"
  };

  /* ---------- Header shadow on scroll ---------- */
  var hdr = document.querySelector(".hdr");
  function onScroll() {
    if (!hdr) return;
    hdr.classList.toggle("scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile drawer ---------- */
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

  /* ---------- Desktop dropdown ---------- */
  document.querySelectorAll(".has-menu").forEach(function (wrap) {
    var btn = wrap.querySelector("button");
    if (!btn) return;
    function close() { wrap.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = wrap.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    wrap.addEventListener("mouseenter", function () { wrap.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    wrap.addEventListener("mouseleave", close);
    document.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  });

  /* ---------- Scroll reveal ---------- */
  var rv = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window && rv.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    rv.forEach(function (el, i) {
      el.style.transitionDelay = (Math.min(i % 4, 3) * 70) + "ms";
      io.observe(el);
    });
  } else {
    rv.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Contact form: client / candidate tabs ---------- */
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var tabs = group.querySelectorAll(".tab");
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute("aria-selected", on ? "true" : "false");
          var panel = document.getElementById(t.getAttribute("aria-controls"));
          if (panel) panel.hidden = !on;
        });
      });
    });
  });

  /* Deep link: /contact.html#candidates opens the candidate tab */
  if (location.hash === "#candidates" || location.hash === "#candidate") {
    var candTab = document.querySelector('.tab[aria-controls="panel-candidate"]');
    if (candTab) candTab.click();
  }

  /* ---------- Form submit ---------- */
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = form.querySelector(".form-msg");
      var btn = form.querySelector('button[type="submit"]');

      /* honeypot */
      if (form.querySelector(".hp input") && form.querySelector(".hp input").value) return;

      var data = {};
      new FormData(form).forEach(function (v, k) { if (k !== "company_website") data[k] = v; });
      data.form = form.getAttribute("data-form");
      data.page = location.pathname;
      data.submitted_at = new Date().toISOString();

      function show(kind, text) {
        if (!msg) { alert(text); return; }
        msg.className = "form-msg " + kind;
        msg.textContent = text;
        msg.scrollIntoView({ behavior: "smooth", block: "center" });
      }

      if (!SITE.FORM_ENDPOINT) {
        /* Staging fallback — never leave a lead with nowhere to go. */
        var lines = Object.keys(data).map(function (k) { return k + ": " + data[k]; }).join("\n");
        window.location.href = "mailto:" + SITE.FALLBACK_EMAIL +
          "?subject=" + encodeURIComponent("Website inquiry — " + data.form) +
          "&body=" + encodeURIComponent(lines);
        show("ok", "Opening your email app so nothing gets lost. You can also call " + SITE.PHONE + ".");
        return;
      }

      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }

      fetch(SITE.FORM_ENDPOINT, {
        method: "POST",
        mode: "no-cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      }).then(function () {
        form.reset();
        show("ok", "Thank you — that's in. Pete or Terry will reach out within one business day. Need it sooner? Call " + SITE.PHONE + ".");
      }).catch(function () {
        show("err", "Something went wrong on our end. Please call " + SITE.PHONE + " or email " + SITE.FALLBACK_EMAIL + ".");
      }).finally(function () {
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label || "Send"; }
      });
    });
  });

  /* ---------- Current year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
