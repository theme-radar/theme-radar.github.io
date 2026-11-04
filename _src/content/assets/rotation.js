(function () {
  var D = JSON.parse(document.getElementById('rrg-data').textContent);
  var box = document.getElementById('rot-chart');
  if (!window.d3 || !box) return;
  var ROT = { bench: 0, trail: 8, sector: 'All', picked: null };
  var BN = ['SPY', 'RSP'];
  var QC = { Leading: 'var(--lead)', Weakening: 'var(--weak)', Lagging: 'var(--lag)', Improving: 'var(--imp)' };
  var PAL = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#6b8e23', '#17becf', '#bab0ac'];
  var secs = Array.from(new Set(D.themes.map(function (t) { return t.s; }))).sort();
  var col = function (s) { return PAL[secs.indexOf(s) % PAL.length]; };
  var tinfo = new Map(D.themes.map(function (t, i) { return [i, t]; }));
  var qOf = function (x, y) { return x >= 100 ? (y >= 100 ? 'Leading' : 'Weakening') : (y >= 100 ? 'Improving' : 'Lagging'); };
  var hOf = function (dx, dy) { var a = Math.atan2(dy, dx) * 180 / Math.PI; return a >= 0 && a <= 90 ? 'Leading' : a > 90 ? 'Improving' : a < -90 ? 'Lagging' : 'Weakening'; };
  var pct = d3.format('+.1%');
  function btns(id, opts, key, lab) {
    var el = document.getElementById(id); el.replaceChildren();
    opts.forEach(function (o) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'fbtn'; b.textContent = lab ? lab(o) : o;
      b.setAttribute('aria-pressed', String(ROT[key] === o));
      b.addEventListener('click', function () { ROT[key] = o; ROT.picked = null; btns(id, opts, key, lab); draw(); });
      el.appendChild(b);
    });
  }
  btns('rot-bench', [0, 1], 'bench', function (o) { return o === 0 ? 'S&P 500 (SPY)' : 'Equal-weight (RSP)'; });
  btns('rot-trail', [4, 8, 12], 'trail', function (o) { return o + ' weeks'; });
  btns('rot-sectors', ['All'].concat(secs), 'sector');
  function pick(i) { ROT.picked = ROT.picked === i ? null : i; draw(); }
  function draw() {
    var pts = D.pts.filter(function (p) {
      var t = tinfo.get(p[0]);
      return p[1] === ROT.bench && p[3] < ROT.trail && (ROT.sector === 'All' || t.s === ROT.sector || p[0] === ROT.picked);
    });
    var by = d3.group(pts, function (p) { return p[0]; });
    var last = d3.max(pts, function (p) { return p[2]; });
    document.getElementById('rot-asof').textContent = last ? 'Latest point: week to ' + d3.utcFormat('%a %-d %b %Y')(new Date(last)) + ' (the latest week may be partial). Benchmark ' + (ROT.bench === 0 ? 'S&P 500 (SPY, cap-weighted)' : 'S&P 500 equal-weight (RSP)') + '. Colour = sector. Tap a dot to highlight a theme.' : '';
    box.replaceChildren();
    var W = box.clientWidth || 600, H = Math.max(340, Math.min(W * 0.82, 640));
    var m = { t: 24, r: 16, b: 34, l: 44 };
    var dx = Math.max(1.2, (d3.max(pts, function (p) { return Math.abs(p[4] - 100); }) || 2) * 1.12);
    var dy = Math.max(1.2, (d3.max(pts, function (p) { return Math.abs(p[5] - 100); }) || 2) * 1.12);
    var x = d3.scaleLinear([100 - dx, 100 + dx], [m.l, W - m.r]);
    var y = d3.scaleLinear([100 - dy, 100 + dy], [H - m.b, m.t]);
    var svg = d3.select(box).append('svg').attr('viewBox', '0 0 ' + W + ' ' + H).attr('width', '100%').attr('height', H)
      .attr('role', 'img').attr('aria-label', 'Relative rotation graph of themes');
    [['Improving', m.l, m.t, x(100), y(100)], ['Leading', x(100), m.t, W - m.r, y(100)], ['Lagging', m.l, y(100), x(100), H - m.b], ['Weakening', x(100), y(100), W - m.r, H - m.b]].forEach(function (q) {
      svg.append('rect').attr('x', q[1]).attr('y', q[2]).attr('width', q[3] - q[1]).attr('height', q[4] - q[2]).attr('fill', QC[q[0]]).attr('fill-opacity', 0.07);
      var right = q[0] === 'Leading' || q[0] === 'Weakening', bottom = q[0] === 'Lagging' || q[0] === 'Weakening';
      svg.append('text').attr('x', right ? q[3] - 8 : q[1] + 8).attr('y', bottom ? q[4] - 8 : q[2] + 18).attr('text-anchor', right ? 'end' : 'start')
        .attr('fill', QC[q[0]]).style('font-size', '13px').style('font-weight', 600).attr('opacity', 0.8).text(q[0]);
    });
    var ax = function (g) { g.selectAll('text').attr('fill', 'var(--mute)').style('font-size', '11px'); g.selectAll('line,path').attr('stroke', 'var(--line)'); };
    svg.append('g').attr('transform', 'translate(0,' + (H - m.b) + ')').call(d3.axisBottom(x).ticks(Math.max(3, Math.floor(W / 90))).tickFormat(d3.format('.1f'))).call(ax);
    svg.append('g').attr('transform', 'translate(' + m.l + ',0)').call(d3.axisLeft(y).ticks(6).tickFormat(d3.format('.1f'))).call(ax);
    svg.append('text').attr('x', W - m.r).attr('y', H - 4).attr('text-anchor', 'end').attr('fill', 'var(--mute)').style('font-size', '11px').text('RS-Ratio: relative strength →');
    svg.append('text').attr('transform', 'translate(' + (m.l + 14) + ',' + (m.t + 30) + ') rotate(-90)').attr('text-anchor', 'end').attr('fill', 'var(--mute)').style('font-size', '11px').text('RS-Momentum ↑');
    svg.append('line').attr('x1', x(100)).attr('x2', x(100)).attr('y1', m.t).attr('y2', H - m.b).attr('stroke', 'var(--mute)').attr('stroke-dasharray', '4 4').attr('opacity', .5);
    svg.append('line').attr('x1', m.l).attr('x2', W - m.r).attr('y1', y(100)).attr('y2', y(100)).attr('stroke', 'var(--mute)').attr('stroke-dasharray', '4 4').attr('opacity', .5);
    var tip = d3.select(box).append('div').attr('class', 'rtip').style('display', 'none');
    var line = d3.line().x(function (p) { return x(p[4]); }).y(function (p) { return y(p[5]); });
    var focus = ROT.picked, heads = [];
    var keys = Array.from(by.keys());
    var order = keys.slice().sort(function (a, b) { return (a === focus) - (b === focus); });
    var busy = ROT.sector === 'All' && focus === null;
    order.forEach(function (k) {
      var s = by.get(k).slice().sort(function (a, b) { return b[3] - a[3]; });
      var t = tinfo.get(k);
      var c = ROT.sector === 'All' ? col(t.s) : PAL[keys.slice().sort().indexOf(k) % PAL.length];
      var dim = focus !== null && k !== focus;
      var g = svg.append('g').attr('opacity', dim ? 0.15 : 1).style('cursor', 'pointer').on('click', function () { pick(k); });
      g.append('path').datum(s).attr('d', line).attr('fill', 'none').attr('stroke', c).attr('stroke-width', k === focus ? 2.5 : busy ? 1 : 1.5).attr('stroke-opacity', busy ? 0.35 : 0.85);
      if (!busy) s.slice(0, -1).forEach(function (p) { g.append('circle').attr('cx', x(p[4])).attr('cy', y(p[5])).attr('r', 2).attr('fill', c).attr('fill-opacity', 0.7); });
      var h = s[s.length - 1], p0 = s[s.length - 2];
      var q = qOf(h[4], h[5]), hd = p0 ? hOf(h[4] - p0[4], h[5] - p0[5]) : '—';
      g.append('circle').attr('cx', x(h[4])).attr('cy', y(h[5])).attr('r', k === focus ? 7 : 5).attr('fill', c).attr('stroke', 'var(--card)').attr('stroke-width', 1.5)
        .on('mousemove', function (ev) {
          var pt = d3.pointer(ev, box);
          tip.style('display', 'block').html('');
          tip.append('div').style('font-weight', 600).text(t.t);
          tip.append('div').attr('class', 'mute').text(t.s + ' · ' + q + ', heading to ' + hd);
          tip.append('div').text(t.l + ' · 5D ' + pct(t.d5) + ' · 20D ' + pct(t.d20));
          var bw = box.clientWidth, tw = tip.node().offsetWidth;
          tip.style('left', Math.min(pt[0] + 12, bw - tw - 4) + 'px').style('top', Math.max(pt[1] - 44, 0) + 'px');
        })
        .on('mouseleave', function () { tip.style('display', 'none'); });
      if (!dim) heads.push({ k: k, name: t.t, x: x(h[4]), y: y(h[5]), pri: k === focus ? 1e9 : Math.hypot(h[4] - 100, h[5] - 100) + (q === 'Improving' && hd === 'Leading' ? 5 : 0) });
    });
    var placed = [], fs = 11;
    var hit = function (bx, by0, w, hh) { return bx < m.l || bx + w > W - m.r || placed.some(function (p) { return bx < p.x + p.w && bx + w > p.x && by0 < p.y + p.h && by0 + hh > p.y; }); };
    heads.sort(function (a, b) { return b.pri - a.pri; }).forEach(function (h) {
      var w = h.name.length * fs * 0.54, hh = fs + 2, by0 = h.y - hh / 2, left = false;
      if (hit(h.x + 8, by0, w, hh)) { if (hit(h.x - 8 - w, by0, w, hh)) return; left = true; }
      placed.push({ x: left ? h.x - 8 - w : h.x + 8, y: by0, w: w, h: hh });
      svg.append('text').attr('x', left ? h.x - 8 : h.x + 8).attr('y', h.y).attr('dy', '0.35em').attr('text-anchor', left ? 'end' : 'start')
        .attr('fill', 'var(--fg)').attr('paint-order', 'stroke').attr('stroke', 'var(--card)').attr('stroke-width', 3)
        .style('font-size', fs + 'px').style('font-weight', h.k === focus ? 600 : 400).style('pointer-events', 'none').text(h.name);
    });
    var pk = document.getElementById('rot-picked');
    if (focus !== null) { var t = tinfo.get(focus); pk.innerHTML = ''; var a = document.createElement('a'); a.href = '/rotation/' + t.slug + '/'; a.textContent = t.t + ': see its names →'; pk.appendChild(a); }
    else pk.textContent = '';
  }
  draw();
  var lw = 0; new ResizeObserver(function () { var w = box.clientWidth; if (w && Math.abs(w - lw) > 20) { lw = w; draw(); } }).observe(box);
})();
