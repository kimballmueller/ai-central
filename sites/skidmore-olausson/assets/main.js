/* Skidmore & Olausson PLLC — interactions */
(function () {
  "use strict";

  // Sticky header shadow on scroll
  const header = document.querySelector(".site-header");
  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("scrolled", window.scrollY > 8);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile nav
  const toggle = document.querySelector(".menu-toggle");
  const panel = document.querySelector(".mobile-panel");
  if (toggle && panel) {
    const close = () => {
      toggle.classList.remove("open");
      panel.classList.remove("open");
      document.body.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
    };
    toggle.addEventListener("click", () => {
      const open = panel.classList.toggle("open");
      toggle.classList.toggle("open", open);
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    panel.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
  }

  // Scroll reveal
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("in"));
  }

  // Current year
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  // Contact / consult forms -> compose a mailto so nothing is lost without a backend
  document.querySelectorAll("form[data-mailto]").forEach((form) => {
    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      const to = form.getAttribute("data-mailto");
      const data = new FormData(form);
      const subject = encodeURIComponent(
        form.getAttribute("data-subject") || "Website inquiry"
      );
      let body = "";
      data.forEach((val, key) => {
        if (!val) return;
        const label = key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, " ");
        body += `${label}: ${val}\n`;
      });
      const note = form.querySelector("[data-note]");
      if (note) note.hidden = false;
      window.location.href = `mailto:${to}?subject=${subject}&body=${encodeURIComponent(body)}`;
    });
  });
})();
