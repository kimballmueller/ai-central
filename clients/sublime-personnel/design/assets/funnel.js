/* =========================================================
   Sublime Personnel — funnel behaviour
   Multi-step intake · cost-of-vacancy calculator · talent network
   ========================================================= */
(function () {
  "use strict";

  var CFG = {
    /* --- PASTE the GHL inbound-webhook URL here to go live --------------
       Every submission below POSTs here as JSON, including partial
       step data. Until it is set, submissions are logged and the UI
       still completes so the prototype is testable end to end.        */
    ENDPOINT: "",
    PHONE: "713-396-0944",
    EMAIL: "pete@sublimepersonnel.com",
    /* The fee ladder is Pete's own, from the Aug 28 call: "if you're going to
       ask us for 15%, we're going to back you up to a 60-day warranty. 20 is
       pretty standard, we're going to give you 90. You want 120 days, this is
       the fee attached to it." Fee and guarantee move together — that is the
       whole point of the control, so never edit one of these without the other. */
    TIERS: [
      { fee: 0.15, warranty: 60,  label: "15%" },
      { fee: 0.20, warranty: 90,  label: "20%" },
      { fee: 0.25, warranty: 120, label: "25%" }
    ],
    DEFAULT_TIER: 1,
    QUARTER_DAYS: 90,
    WORK_DAYS: 260
  };

  /* Whatever the visitor has configured in the calculator, so any form on the
     page can carry it. Populated by the calculator; empty everywhere else. */
  var calcState = null;

  function post(payload) {
    payload.page = location.pathname;
    payload.at = new Date().toISOString();
    if (!CFG.ENDPOINT) { console.log("[funnel] no endpoint set — payload:", payload); return Promise.resolve(); }
    return fetch(CFG.ENDPOINT, {
      method: "POST", mode: "no-cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).catch(function (e) { console.warn("[funnel] post failed", e); });
  }

  /* GA4 / analytics hook — every step fires so drop-off is visible */
  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
    console.log("[track]", name, params || {});
  }

  var money = function (n) {
    return "$" + Math.round(n).toLocaleString("en-US");
  };

  /* =====================================================
     1. MULTI-STEP INTAKE
     ===================================================== */
  var wiz = document.querySelector("[data-wizard]");
  if (wiz) {
    var panels = Array.prototype.slice.call(wiz.querySelectorAll(".step-panel")),
        bar    = wiz.querySelector(".wiz-bar i"),
        counter= wiz.querySelector("[data-count]"),
        backBt = wiz.querySelector(".back"),
        nextBt = wiz.querySelector("[data-next]"),
        done   = wiz.querySelector(".wiz-done"),
        inner  = wiz.querySelector(".wiz-inner"),
        idx = 0,
        total = panels.length,
        KEY = "sp_intake";

    /* restore an abandoned run */
    try {
      var saved = JSON.parse(sessionStorage.getItem(KEY) || "{}");
      Object.keys(saved).forEach(function (k) {
        var el = wiz.querySelector('[name="' + k + '"]');
        if (!el) return;
        if (el.type === "radio") {
          var hit = wiz.querySelector('[name="' + k + '"][value="' + saved[k] + '"]');
          if (hit) hit.checked = true;
        } else { el.value = saved[k]; }
      });
    } catch (e) {}

    function collect() {
      var out = {};
      new FormData(wiz.querySelector("form")).forEach(function (v, k) {
        if (k !== "company_website") out[k] = v;
      });
      return out;
    }

    function persist() {
      try { sessionStorage.setItem(KEY, JSON.stringify(collect())); } catch (e) {}
    }

    function validate(panel) {
      var ok = true;
      panel.querySelectorAll("[data-required]").forEach(function (group) {
        var name = group.getAttribute("data-required");
        var els = wiz.querySelectorAll('[name="' + name + '"]');
        var filled = Array.prototype.some.call(els, function (el) {
          return el.type === "radio" ? el.checked : String(el.value).trim() !== "";
        });
        var custom = true;
        var first = els[0];
        if (filled && first && first.type === "email") {
          custom = /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(first.value.trim());
        }
        group.classList.toggle("bad", !(filled && custom));
        if (first && first.setAttribute) first.setAttribute("aria-invalid", (filled && custom) ? "false" : "true");
        if (!(filled && custom)) ok = false;
      });
      var bad = panel.querySelector(".bad [name]");
      if (bad) bad.focus();
      return ok;
    }

    function show(n) {
      panels.forEach(function (p, i) { p.hidden = i !== n; });
      idx = n;
      if (bar) bar.style.width = ((n + 1) / total * 100) + "%";
      if (counter) counter.textContent = "Step " + (n + 1) + " of " + total;
      if (backBt) backBt.hidden = n === 0;
      if (nextBt) nextBt.querySelector("span").textContent = n === total - 1 ? "Send it to Pete and Terry" : "Continue";
      var h = panels[n].querySelector("h2");
      if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
      track("intake_step_view", { step: n + 1 });
    }

    wiz.addEventListener("change", persist);
    wiz.addEventListener("input", persist);

    /* selecting a tile on step 1 advances automatically */
    wiz.querySelectorAll('[data-advance] input[type="radio"]').forEach(function (r) {
      r.addEventListener("change", function () {
        persist();
        if (idx === 0 && validate(panels[0])) setTimeout(function () { show(1); }, 180);
      });
    });

    if (backBt) backBt.addEventListener("click", function () { if (idx > 0) show(idx - 1); });

    wiz.querySelector("form").addEventListener("submit", function (e) {
      e.preventDefault();
      if (wiz.querySelector('.hp input') && wiz.querySelector('.hp input').value) return;
      if (!validate(panels[idx])) return;

      if (idx < total - 1) {
        track("intake_step_complete", { step: idx + 1 });
        /* partial capture: a half-finished form is still a lead */
        post({ form: "employer_intake_partial", step: idx + 1, data: collect() });
        show(idx + 1);
        return;
      }

      var data = collect();
      nextBt.disabled = true;
      nextBt.querySelector("span").textContent = "Sending…";
      track("intake_submit", { industry: data.industry, hires_per_year: data.volume });
      post({ form: "employer_intake", complete: true, data: data }).then(function () {
        try { sessionStorage.removeItem(KEY); } catch (e) {}
        if (inner) inner.hidden = true;
        if (bar) bar.style.width = "100%";
        if (done) {
          done.hidden = false;
          var nm = done.querySelector("[data-name]");
          if (nm && data.name) nm.textContent = String(data.name).split(" ")[0];
          done.querySelector("h2").setAttribute("tabindex", "-1");
          done.querySelector("h2").focus();
        }
      });
    });

    show(0);
  }

  /* =====================================================
     2. COST-OF-VACANCY CALCULATOR
     ===================================================== */
  var calc = document.querySelector("[data-calc]");
  if (calc) {
    var sal   = calc.querySelector("#salary"),
        days  = calc.querySelector("#daysopen"),
        hires = calc.querySelector("#hires"),
        mult  = calc.querySelector("#multiplier"),
        title = calc.querySelector("#jobtitle"),
        tiers = [].slice.call(calc.querySelectorAll("input[name=tier]"));

    function currentTier() {
      for (var i = 0; i < tiers.length; i++) {
        if (tiers[i].checked) return CFG.TIERS[+tiers[i].value] || CFG.TIERS[CFG.DEFAULT_TIER];
      }
      return CFG.TIERS[CFG.DEFAULT_TIER];
    }

    function run() {
      var S = +sal.value, D = +days.value, H = +hires.value, M = +mult.value;
      var T = currentTier();

      var dailyValue  = (S * M) / CFG.WORK_DAYS;
      var vacancyCost = dailyValue * D;
      var quarterCost = dailyValue * CFG.QUARTER_DAYS;
      var fee         = S * T.fee;
      var breakEven   = fee / dailyValue;    /* days of vacancy that equal the fee */
      var annualFee   = fee * H;
      var annualVac   = quarterCost * H;     /* H seats, each empty for a quarter */

      calc.querySelector("[data-out=salary]").textContent = money(S);
      calc.querySelector("[data-out=days]").textContent   = D + (D === 1 ? " day" : " days");
      calc.querySelector("[data-out=hires]").textContent  = H + (H === 1 ? " hire" : " hires") + " / year";
      calc.querySelector("[data-out=mult]").textContent   = M.toFixed(1) + "\u00d7";

      calc.querySelector("[data-out=daily]").textContent   = money(dailyValue);
      calc.querySelector("[data-out=vacancy]").textContent = money(vacancyCost);
      calc.querySelector("[data-out=quarter]").textContent = money(quarterCost);
      calc.querySelector("[data-out=fee]").textContent     = money(fee);
      calc.querySelector("[data-out=feelabel]").innerHTML  =
        "Our fee at " + T.label + " \u00b7 " + T.warranty + "\u2011day guarantee";
      calc.querySelector("[data-out=breakeven]").textContent = Math.round(breakEven) + " days";

      var v = calc.querySelector("[data-out=verdict]");
      var lead;
      if (vacancyCost > fee) {
        lead = "This seat has already cost you <strong>" + money(vacancyCost - fee) +
          " more</strong> than our fee to fill it. Every further day adds <strong>" +
          money(dailyValue) + "</strong>.";
      } else {
        lead = "The fee overtakes the cost of the empty seat at <strong>" + Math.round(breakEven) +
          " days</strong>. You are at " + D + ".";
      }
      /* The volume slider earns its place here: fees are a known, bounded cost;
         the seats sitting empty are not. */
      v.innerHTML = lead + " <span class=\"vol\">At " + H + (H === 1 ? " role" : " roles") +
        " a year our fees come to <strong>" + money(annualFee) +
        "</strong>. Those same seats each sitting empty a quarter costs you <strong>" +
        money(annualVac) + "</strong>.</span>";

      calcState = {
        job_title:   title && title.value.trim() ? title.value.trim() : null,
        salary:      S,
        days_open:   D,
        roles_per_year: H,
        value_multiplier: M,
        fee_tier:    T.label,
        guarantee_days: T.warranty,
        daily_cost:  Math.round(dailyValue),
        cost_so_far: Math.round(vacancyCost),
        quarterly_loss: Math.round(quarterCost),
        fee_quoted:  Math.round(fee),
        breakeven_days: Math.round(breakEven)
      };
    }

    [sal, days, hires, mult].concat(tiers).forEach(function (el) {
      el.addEventListener("input", run);
      el.addEventListener("change", function () {
        track("calc_adjust", { field: el.name === "tier" ? "tier" : el.id, value: el.value });
      });
    });
    if (title) title.addEventListener("input", run);
    run();
  }

  /* =====================================================
     3. JOB BOARD FILTERS
     Pure client-side narrowing over rows already in the DOM. Every row carries
     its own data-state / data-practice / data-band, so adding a filter is a new
     <select data-filter="..."> and a matching attribute — no JS change.
     ===================================================== */
  var board = document.querySelector("[data-jobs]");
  if (board) {
    var jobList  = document.querySelector("[data-jobs-list]"),
        jobRows  = [].slice.call(jobList.querySelectorAll(".job")),
        countEl  = document.querySelector("[data-jobs-count]"),
        nounEl   = document.querySelector("[data-jobs-noun]"),
        emptyEl  = document.querySelector("[data-jobs-empty]"),
        selects  = [].slice.call(board.querySelectorAll("[data-filter]"));

    function filterJobs() {
      var active = {};
      selects.forEach(function (sel) {
        if (sel.value) active[sel.getAttribute("data-filter")] = sel.value;
      });

      var shown = 0;
      jobRows.forEach(function (row) {
        var hit = Object.keys(active).every(function (k) {
          return row.getAttribute("data-" + k) === active[k];
        });
        row.hidden = !hit;
        if (hit) shown++;
      });

      countEl.textContent = shown;
      nounEl.textContent = shown === 1 ? "role" : "roles";
      emptyEl.hidden = shown !== 0;
      jobList.hidden = shown === 0;
    }

    selects.forEach(function (sel) {
      sel.addEventListener("change", function () {
        filterJobs();
        track("jobs_filter", { field: sel.getAttribute("data-filter"), value: sel.value });
      });
    });
    filterJobs();
  }

  /* =====================================================
     4. SIMPLE FORMS (talent network, calculator email capture)
     ===================================================== */
  document.querySelectorAll("form[data-simple]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector(".hp input") && form.querySelector(".hp input").value) return;

      var ok = true;
      form.querySelectorAll("[data-required]").forEach(function (g) {
        var el = g.querySelector("[name]");
        var good = el && String(el.value).trim() !== "";
        if (good && el.type === "email") good = /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(el.value.trim());
        g.classList.toggle("bad", !good);
        if (el) el.setAttribute("aria-invalid", good ? "false" : "true");
        if (!good) ok = false;
      });
      if (!ok) { var b = form.querySelector(".bad [name]"); if (b) b.focus(); return; }

      var data = {};
      new FormData(form).forEach(function (v, k) { if (k !== "company_website") data[k] = v; });
      /* Forms sitting around the calculator send the scenario the visitor built
         with them — Pete asked for exactly this: "it would tell us what salary
         range they're looking at, how long the position's been open." */
      if (form.hasAttribute("data-calc-context") && calcState) {
        Object.keys(calcState).forEach(function (k) { if (calcState[k] !== null) data[k] = calcState[k]; });
      }
      var btn = form.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; btn.dataset.l = btn.textContent; btn.textContent = "Sending…"; }
      track(form.getAttribute("data-simple") + "_submit", {});

      post({ form: form.getAttribute("data-simple"), data: data }).then(function () {
        var okBox = form.querySelector(".form-ok");
        if (okBox) {
          form.querySelectorAll(".field, .btns, button[type=submit], .form-note").forEach(function (n) { n.hidden = true; });
          okBox.hidden = false;
          okBox.setAttribute("tabindex", "-1");
          okBox.focus();
        }
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.l; }
      });
    });
  });
})();
