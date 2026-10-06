/*
 * Hero decoration: concentric, slightly irregular isotherm lines radiating from a heat source,
 * like the temperature-field diagrams used in heat transfer. Purely visual (the SVG is aria-hidden).
 * Without JavaScript the hero simply shows its CSS glow instead.
 */
(function () {
  'use strict';

  var svg = document.getElementById('heat-field');
  if (!svg) return;

  var NS = 'http://www.w3.org/2000/svg';
  var SOURCE = { x: 1150, y: 700 };                               // heat source, in viewBox units
  var RADII = [70, 120, 175, 235, 300, 375, 460, 555, 660, 775, 900];
  var POINTS = 44;                                                 // samples per contour
  var STOPS = [                                                    // hot -> cool along the lines
    [0, [248, 180, 49]],
    [0.35, [238, 122, 31]],
    [0.7, [194, 55, 27]],
    [1, [138, 32, 20]]
  ];

  function lerp(a, b, t) { return a + (b - a) * t; }

  function colorAt(t) {
    for (var i = 1; i < STOPS.length; i++) {
      if (t <= STOPS[i][0]) {
        var u = (t - STOPS[i - 1][0]) / (STOPS[i][0] - STOPS[i - 1][0]);
        var a = STOPS[i - 1][1], b = STOPS[i][1];
        return 'rgb(' + [0, 1, 2].map(function (c) { return Math.round(lerp(a[c], b[c], u)); }).join(',') + ')';
      }
    }
    return 'rgb(' + STOPS[STOPS.length - 1][1].join(',') + ')';
  }

  /** Points around the source; outer lines get more irregular, as real isotherms do. */
  function contour(k, radius) {
    var t = k / (RADII.length - 1);
    var a2 = 0.018 + 0.05 * t, a3 = 0.012 + 0.04 * t, a5 = 0.008 + 0.02 * t;
    var p2 = 0.9 + k * 0.55, p3 = 2.1 + k * 0.8, p5 = 0.4 + k * 1.3;
    var pts = [];
    for (var i = 0; i < POINTS; i++) {
      var th = (2 * Math.PI * i) / POINTS;
      var r = radius * (1 + a2 * Math.sin(2 * th + p2) + a3 * Math.sin(3 * th + p3) + a5 * Math.sin(5 * th + p5));
      pts.push([SOURCE.x + r * Math.cos(th) * 1.18, SOURCE.y + r * Math.sin(th) * 0.9]);
    }
    return pts;
  }

  /** Closed Catmull-Rom spline converted to cubic Bezier segments. */
  function smoothPath(pts) {
    var n = pts.length;
    var d = 'M' + pts[0][0].toFixed(1) + ' ' + pts[0][1].toFixed(1);
    for (var i = 0; i < n; i++) {
      var p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      d += 'C' + [
        p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
        p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6,
        p2[0], p2[1]
      ].map(function (v) { return v.toFixed(1); }).join(' ');
    }
    return d + 'Z';
  }

  RADII.forEach(function (radius, k) {
    var t = k / (RADII.length - 1);
    var path = document.createElementNS(NS, 'path');
    path.setAttribute('d', smoothPath(contour(k, radius)));
    path.setAttribute('pathLength', '1');
    path.setAttribute('stroke', colorAt(t));
    path.setAttribute('stroke-opacity', lerp(0.85, 0.26, t).toFixed(2));
    path.setAttribute('stroke-width', lerp(2.2, 1.4, t).toFixed(2));
    path.style.setProperty('--i', k);                              // used by CSS to stagger the draw-in
    svg.appendChild(path);
  });
})();
