(function () {
  var media = window.POGGKT_MEDIA || {};
  var base = document.currentScript ? document.currentScript.src : location.href;
  var part = document.body.getAttribute("data-part") || "";

  function youtubeId(url) {
    var m = /(?:youtu\.be\/|[?&]v=|\/shorts\/|\/embed\/|\/live\/)([\w-]{11})/.exec(url || "");
    return m ? m[1] : "";
  }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text) node.textContent = text;
    return node;
  }

  function outLink(cls, url) {
    var a = el("a", cls);
    a.href = url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    return a;
  }

  // Main video: swap the reserved strip for a YouTube card.
  var slot = document.getElementById("video");
  var url = ((media.video || {})[part] || "").trim();
  if (slot && url) {
    var card = outLink("video", url);
    var id = youtubeId(url);
    if (id) {
      var thumb = el("img", "thumb");
      thumb.alt = "";
      thumb.src = "https://i.ytimg.com/vi/" + id + "/hqdefault.jpg";
      card.appendChild(thumb);
    }
    var play = el("span", "play");
    play.setAttribute("aria-hidden", "true");
    card.appendChild(play);
    card.appendChild(el("span", "video-label", "Watch on YouTube"));
    slot.parentNode.replaceChild(card, slot);
  }

  // Picture slots: empty until a photo is set. Steps can also get a video button.
  function fill(shot) {
    var key = shot.getAttribute("data-slot");
    var photo = ((media.photo || {})[key] || "").trim();
    var clip = ((media.stepVideo || {})[key] || "").trim();
    if (photo) {
      var img = el("img");
      img.alt = shot.getAttribute("data-alt") || "";
      img.decoding = "async";
      img.onload = function () { shot.classList.add("has-photo"); };
      img.onerror = function () { if (img.parentNode) img.parentNode.removeChild(img); };
      img.src = new URL(photo, base).href;
      shot.appendChild(img);
    }
    if (clip) {
      var btn = outLink("shot-play", clip);
      var icon = el("span", "play");
      icon.setAttribute("aria-hidden", "true");
      btn.appendChild(icon);
      btn.appendChild(el("span", "", "Watch this step"));
      shot.parentNode.insertBefore(btn, shot.nextSibling);
    }
  }

  var shots = document.querySelectorAll("[data-slot]");
  for (var i = 0; i < shots.length; i++) fill(shots[i]);
})();
