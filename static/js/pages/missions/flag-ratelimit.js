/**
 * Digital Day CTF — Flag Rate-Limit Feedback
 * =============================================
 * Intercepts flag-submit button clicks and, when the server responds
 * with HTTP 429 (rate-limited), replaces the page-redirect with an
 * in-modal animated countdown so players never lose their context.
 *
 * Compatible with the existing Bootstrap 2 / jQuery stack.
 */
(function ($) {
  "use strict";

  /* ------------------------------------------------------------------ */
  /* Constants                                                            */
  /* ------------------------------------------------------------------ */
  var SUBMIT_BUTTON_IDS = [
    "#capture-text-flag-submit",
    "#capture-choice-flag-submit",
    "#capture-file-flag-submit",
    "#capture-text-flag-box-submit",
  ];

  var FORM_IDS = [
    "#capture-text-flag-form",
    "#capture-choice-flag-form",
    "#capture-file-flag-form",
    "#capture-text-flag-box-form",
  ];

  /* ------------------------------------------------------------------ */
  /* Rate-limit UI overlay                                                */
  /* ------------------------------------------------------------------ */
  var OVERLAY_ID = "nexus-ratelimit-overlay";

  function buildOverlay() {
    if ($("#" + OVERLAY_ID).length) return;

    var html = [
      '<div id="' + OVERLAY_ID + '" style="',
      "  display:none; position:fixed; top:0; left:0; width:100%; height:100%;",
      "  background:rgba(0,0,0,0.82); z-index:9999;",
      "  display:flex; align-items:center; justify-content:center;",
      '  backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);" >',
      '  <div style="',
      "    text-align:center; font-family:'JetBrains Mono',monospace;",
      "    border:1px solid rgba(57,255,20,0.4);",
      "    background:rgba(10,10,10,0.9);",
      "    border-radius:16px; padding:48px 56px;",
      '    box-shadow:0 0 40px rgba(57,255,20,0.25);">',
      '    <div style="font-size:13px; letter-spacing:3px; color:#39ff14; margin-bottom:14px;">',
      "      ⚠ NEXUS · PROTECTION ACTIVE",
      "    </div>",
      '    <div id="nexus-rl-countdown" style="',
      "      font-size:72px; font-weight:700; color:#39ff14;",
      '      text-shadow:0 0 24px rgba(57,255,20,0.9); line-height:1;">00</div>',
      '    <div style="margin-top:12px; font-size:13px; color:rgba(255,255,255,0.6);">',
      "      Trop de tentatives détectées.",
      "    </div>",
      '    <div style="margin-top:4px; font-size:12px; color:rgba(255,255,255,0.4);">',
      "      Le bouton se réactivera automatiquement.",
      "    </div>",
      '    <div style="margin-top:24px;">',
      '      <div id="nexus-rl-bar-wrap" style="',
      "        width:220px; height:4px; background:rgba(255,255,255,0.1);",
      '        border-radius:4px; margin:0 auto; overflow:hidden;">',
      '        <div id="nexus-rl-bar" style="',
      "          height:100%; width:100%; background:#39ff14;",
      '          transition:width linear 1s; border-radius:4px;"></div>',
      "      </div>",
      "    </div>",
      "  </div>",
      "</div>",
    ].join("");

    $("body").append(html);
    /* Start hidden (display:none overrides the inline flex above) */
    $("#" + OVERLAY_ID).css("display", "none");
  }

  /* Lock all submit buttons and show an inline spinner */
  function lockButtons(seconds) {
    $(SUBMIT_BUTTON_IDS.join(",")).each(function () {
      var $btn = $(this);
      $btn.data("original-html", $btn.html());
      $btn
        .prop("disabled", true)
        .css("opacity", "0.4")
        .html('<i class="fa fa-lock"></i> ' + seconds + "s");
    });
  }

  function unlockButtons() {
    $(SUBMIT_BUTTON_IDS.join(",")).each(function () {
      var $btn = $(this);
      $btn
        .prop("disabled", false)
        .css("opacity", "1")
        .html($btn.data("original-html") || "Submit");
    });
  }

  /* Show the full-screen overlay countdown */
  function showCountdown(seconds) {
    buildOverlay();

    var $overlay = $("#" + OVERLAY_ID);
    var $counter = $("#nexus-rl-countdown");
    var $bar = $("#nexus-rl-bar");
    var total = seconds;
    var remaining = seconds;

    $overlay.css("display", "flex");
    lockButtons(remaining);

    /* Reset bar to full */
    $bar.css({ transition: "none", width: "100%" });

    /* Kick off shrink in the next frame so transition fires */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        $bar.css({
          transition: "width linear " + total + "s",
          width: "0%",
        });
      });
    });

    /* Tick every second */
    var interval = setInterval(function () {
      remaining -= 1;
      $counter.text(remaining < 10 ? "0" + remaining : remaining);
      lockButtons(remaining);

      if (remaining <= 0) {
        clearInterval(interval);
        $overlay.css("display", "none");
        unlockButtons();
      }
    }, 1000);

    /* Initial display */
    $counter.text(remaining < 10 ? "0" + remaining : remaining);
  }

  /* ------------------------------------------------------------------ */
  /* Parse Retry-After from a server-rendered info message               */
  /* ------------------------------------------------------------------ */
  function extractRetryAfter(responseText) {
    /* 1) HTTP Retry-After header (when AJAX is used) */
    /* 2) Fallback: parse from the French message that the server injects */
    var match = (responseText || "").match(/patienter\s+(\d+)\s+seconde/i);
    if (match) return parseInt(match[1], 10);
    return 30; /* safe default */
  }

  /* ------------------------------------------------------------------ */
  /* AJAX form submission wrapper                                         */
  /* ------------------------------------------------------------------ */
  function interceptForm($form, $submitBtn) {
    $submitBtn.on("click", function (e) {
      e.preventDefault();

      var formData = new FormData($form[0]);

      $.ajax({
        url: $form.attr("action"),
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        complete: function (xhr) {
          if (xhr.status === 429) {
            /* Rate limited — parse wait time */
            var retryAfter =
              parseInt(xhr.getResponseHeader("Retry-After"), 10) ||
              extractRetryAfter(xhr.responseText) ||
              30;
            showCountdown(retryAfter);
          } else {
            /* Normal response — replace page content or redirect */
            if (
              xhr.getResponseHeader("Content-Type") &&
              xhr.getResponseHeader("Content-Type").indexOf("text/html") === 0
            ) {
              /* Full-page replacement (standard Tornado pattern) */
              document.open();
              document.write(xhr.responseText);
              document.close();
            } else {
              /* Fallback: just reload */
              location.reload();
            }
          }
        },
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* Init on DOM ready                                                    */
  /* ------------------------------------------------------------------ */
  $(function () {
    buildOverlay();

    /* Wire text, choice, file flag modals */
    var pairs = [
      ["#capture-text-flag-form", "#capture-text-flag-submit"],
      ["#capture-choice-flag-form", "#capture-choice-flag-submit"],
      ["#capture-file-flag-form", "#capture-file-flag-submit"],
      ["#capture-text-flag-box-form", "#capture-text-flag-box-submit"],
    ];

    pairs.forEach(function (pair) {
      var $form = $(pair[0]);
      var $btn = $(pair[1]);
      if ($form.length && $btn.length) {
        interceptForm($form, $btn);
      }
    });
  });
})(jQuery);
