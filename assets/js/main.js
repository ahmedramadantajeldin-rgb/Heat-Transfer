(function () {
  "use strict";

  var course = window.COURSE || {};
  var chapters = (window.CHAPTERS || []).slice().sort(function (a, b) { return a.number - b.number; });

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function isAvailable(ch) { return ch.status === "available" && !!ch.href; }

  function buildCard(ch) {
    var available = isAvailable(ch);
    var heading = ch.title || "Chapter " + ch.number;

    var item = el("li", "chapter " + (available ? "is-available" : "is-soon"));
    item.appendChild(el("span", "node", String(ch.number)));

    var card = el("article", "card");
    var head = el("div", "card-head");
    head.appendChild(el("span", "card-no", ch.title ? "Chapter " + ch.number : ""));
    head.appendChild(el("span", "badge", available ? "Available" : "Coming soon"));
    card.appendChild(head);

    card.appendChild(el("h3", "card-title", heading));
    if (ch.titleAr) {
      var ar = el("p", "card-ar", ch.titleAr);
      ar.lang = "ar"; ar.dir = "rtl";
      card.appendChild(ar);
    }
    if (ch.summary) card.appendChild(el("p", "card-text", ch.summary));

    if (ch.topics && ch.topics.length) {
      var chips = el("ul", "chips");
      ch.topics.forEach(function (t) { chips.appendChild(el("li", "", t)); });
      card.appendChild(chips);
    }

    var foot = el("div", "card-foot");
    if (available) {
      var open = el("a", "btn btn-primary", "Open Chapter " + ch.number);
      open.href = encodeURI(ch.href);
      foot.appendChild(open);
      if (ch.sections) foot.appendChild(el("span", "card-meta", ch.sections + " sections"));
    } else {
      var off = el("span", "btn btn-disabled", "Under development");
      off.setAttribute("aria-disabled", "true");
      foot.appendChild(off);
    }
    card.appendChild(foot);

    item.appendChild(card);
    return item;
  }

  if (course.title) {
    document.getElementById("course-title").textContent = course.title;
    document.title = course.title + " | Course Home";
  }
  document.getElementById("course-subtitle").textContent = course.subtitle || "";

  var list = document.getElementById("chapter-list");
  chapters.forEach(function (ch) { list.appendChild(buildCard(ch)); });

  var open = chapters.filter(isAvailable);
  var soon = chapters.length - open.length;
  document.getElementById("chapters-note").textContent =
    open.length + " available" + (soon ? ", " + soon + " coming soon" : "");

  if (open.length) {
    var start = document.getElementById("start-link");
    start.textContent = "Open Chapter " + open[0].number;
    start.href = encodeURI(open[0].href);
    start.hidden = false;
  }
})();
