/*
 * Home page behaviour: builds the chapter cards from window.CHAPTERS (see chapters.js)
 * and points the hero shortcut at the first available chapter.
 */
(function () {
  'use strict';

  var grid = document.getElementById('chapter-grid');
  if (!grid || !Array.isArray(window.CHAPTERS)) return;

  /** Create an element with optional class name and text. Text is always set as text, never HTML. */
  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  /** Encode spaces etc. in a relative path (e.g. "Chapter 1/chapter1.html") without double-encoding. */
  function toUrl(path) {
    return path.indexOf('%') === -1 ? encodeURI(path) : path;
  }

  /** A chapter is only treated as available when it also has a page to open. */
  function isAvailable(chapter) {
    return chapter.status === 'available' && typeof chapter.href === 'string' && chapter.href !== '';
  }

  function statusPill(available) {
    var pill = el('p', 'status-pill ' + (available ? 'is-lit' : 'is-unlit'));
    pill.appendChild(el('span', 'status-dot'));
    pill.appendChild(el('span', null, available ? 'Available' : 'Coming soon'));
    return pill;
  }

  function heading(chapter, available) {
    var h3 = el('h3', 'card-heading');
    var lockup = el('span', 'card-chapter');
    lockup.appendChild(document.createTextNode('Chapter '));
    lockup.appendChild(el('span', 'card-num', String(chapter.number)));
    h3.appendChild(lockup);
    if (available && chapter.title) {
      h3.appendChild(document.createTextNode(' '));
      h3.appendChild(el('span', 'card-title', chapter.title));
    }
    return h3;
  }

  function topicList(topics) {
    var list = el('ul', 'topics');
    list.setAttribute('aria-label', 'Topics covered');
    topics.forEach(function (topic) {
      list.appendChild(el('li', null, topic));
    });
    return list;
  }

  function buildCard(chapter) {
    var available = isAvailable(chapter);
    var card = el('li', 'chapter-card ' + (available ? 'is-available' : 'is-soon'));

    card.appendChild(statusPill(available));
    card.appendChild(heading(chapter, available));

    if (available) {
      if (chapter.description) card.appendChild(el('p', 'card-text', chapter.description));
      if (chapter.topics && chapter.topics.length) card.appendChild(topicList(chapter.topics));
    } else {
      card.appendChild(
        el('p', 'card-text', 'This chapter is under development and will be added later.')
      );
    }

    var footer = el('div', 'card-footer');
    if (available) {
      if (chapter.sections) footer.appendChild(el('span', 'card-meta', chapter.sections + ' sections'));
      var link = el('a', 'btn btn-primary card-link', 'Open Chapter ' + chapter.number);
      link.href = toUrl(chapter.href);
      footer.appendChild(link);
    } else {
      var disabled = el('button', 'btn btn-disabled', 'Coming soon');
      disabled.type = 'button';
      disabled.disabled = true;
      footer.appendChild(disabled);
    }
    card.appendChild(footer);
    return card;
  }

  var chapters = window.CHAPTERS.slice().sort(function (a, b) {
    return a.number - b.number;
  });

  chapters.forEach(function (chapter) {
    grid.appendChild(buildCard(chapter));
  });

  // Hero shortcut: send visitors straight to the first available chapter.
  var first = chapters.filter(isAvailable)[0];
  var start = document.getElementById('hero-start');
  if (first && start) {
    start.href = toUrl(first.href);
    start.textContent = 'Open Chapter ' + first.number;
    start.hidden = false;
  }
})();
