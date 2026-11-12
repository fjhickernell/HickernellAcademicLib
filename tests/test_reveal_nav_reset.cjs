const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const vm = require('node:vm');

const source = readFileSync(path.join(__dirname, '../classlib/quarto/slides/reveal-nav-reset.html'), 'utf8')
  .replace(/^<script>\s*/, '').replace(/\s*<\/script>\s*$/, '');

function deck(initial = { h: 0, v: 0 }, ready = true) {
  let current = { ...initial }, time = 0;
  const handlers = {}, windowHandlers = {}, documentHandlers = {}, polls = [];
  const target = { closest: () => ({ h: 2, v: 3 }) };
  const window = {
    location: new URL('https://example.org/deck.html'),
    addEventListener(name, handler) { (windowHandlers[name] ||= []).push(handler); }
  };
  const document = {
    getElementById(id) { return id === 'example' ? target : null; },
    addEventListener(name, handler) { (documentHandlers[name] ||= []).push(handler); }
  };
  const Reveal = {
    getIndices(slide) { return { ...(slide || current) }; },
    isReady: () => ready,
    on(name, handler) { (handlers[name] ||= []).push(handler); },
    slide(h, v, f) {
      current = { h, v, f };
      for (const handler of handlers.slidechanged || []) handler();
    }
  };
  vm.runInNewContext(source, {
    window: Object.assign(window, { Reveal }), document, Reveal, URL,
    navigator: { userAgent: 'test' }, performance: { now: () => time },
    setInterval: fn => polls.push(fn), setTimeout() { throw Error('unexpected retry'); }
  });
  return {
    Reveal,
    indices: () => current,
    poll() { time += 60; for (const fn of polls) fn(); },
    start() { ready = true; for (const fn of handlers.ready || []) fn(); },
    hash(hash, late = false) {
      const newURL = new URL(hash, window.location).href;
      window.location = new URL(newURL);
      // Simulate a browser/Reveal listener that already reset the destination.
      if (late) Reveal.slide(2, 3);
      for (const fn of windowHandlers.hashchange || []) fn({ newURL });
    },
    click(hash) {
      const href = new URL(hash, window.location).href;
      for (const fn of documentHandlers.click || []) fn({ target: { closest: () => ({ href }) } });
      Reveal.slide(2, 3);
    }
  };
}

test('initial deep link survives initialization', () => {
  const d = deck({ h: 0, v: 0 }, false);
  d.poll();
  d.Reveal.slide(2, 3);
  d.start();
  d.poll();
  assert.equal(d.indices().v, 3);
});

test('horizontal arrows reset carried vertical state, including delayed carry', () => {
  const d = deck({ h: 1, v: 2 });
  d.poll();
  d.Reveal.slide(2, 4);
  assert.equal(d.indices().v, 0);
  d.Reveal.slide(2, 5);
  assert.equal(d.indices().v, 0);
});

test('a cross-section link to a nested heading preserves its child slide', () => {
  const d = deck({ h: 1, v: 2 });
  d.poll();
  d.click('#/example');
  d.poll();
  assert.equal(d.indices().v, 3);
  d.Reveal.slide(3, 2);
  assert.equal(d.indices().v, 0);
});

test('address/history hash restores its target even after an earlier reset', () => {
  const d = deck({ h: 1, v: 2 });
  d.poll();
  d.hash('#/example', true);
  d.poll();
  assert.equal(d.indices().v, 3);
  d.hash('#/4/2/1');
  assert.equal(d.indices().h, 4);
  assert.equal(d.indices().v, 2);
  assert.equal(d.indices().f, 1);
});

test('queued hash changes settle on the latest target without replaying stale URLs', () => {
  let current = { h: 1, v: 2 }, time = 0;
  const url = new URL('https://example.org/deck.html#/initial');
  const slides = {
    initial: { h: 1, v: 2 },
    earlier: { h: 2, v: 3 },
    latest: { h: 3, v: 4 },
    overview: { h: 3, v: 0 }
  };
  const handlers = {}, hashHandlers = [], pending = [], polls = [];
  const location = {
    get hash() { return url.hash; },
    set hash(hash) {
      const oldURL = url.href;
      url.hash = hash;
      // Browsers queue a separate event for every changed hash; event.newURL
      // can therefore be older than location.hash when the event is delivered.
      if (url.href !== oldURL) pending.push({ oldURL, newURL: url.href });
    }
  };
  const window = {
    location,
    addEventListener(name, handler, capture = false) {
      if (name === 'hashchange') hashHandlers.push({ handler, capture });
    }
  };
  const document = {
    getElementById(id) { return slides[id] ? { closest: () => slides[id] } : null; },
    addEventListener() {}
  };
  const Reveal = {
    getIndices(slide) { return { ...(slide || current) }; },
    isReady: () => true,
    on(name, handler) { (handlers[name] ||= []).push(handler); },
    slide(h, v = 0, f) {
      const changed = h !== current.h || v !== current.v;
      current = { h, v, f };
      if (changed) for (const handler of handlers.slidechanged || []) handler();
      // Reveal writes the CURRENT slide's URL after slidechanged callbacks,
      // including callbacks that perform a nested slide() call.
      const named = Object.keys(slides).find(id =>
        slides[id].h === current.h && slides[id].v === current.v);
      location.hash = '/' + (named || current.h + (current.v ? '/' + current.v : ''));
    }
  };
  // At the window target, Reveal's earlier hash listener may run before the
  // helper's listener despite capture=true. It reads the current location.
  window.addEventListener('hashchange', () => {
    const hash = location.hash.replace(/^#\/?/, '');
    const parts = hash.split('/').map(Number);
    const destination = slides[hash] || { h: parts[0], v: parts[1] || 0 };
    if (destination.h !== current.h || destination.v !== current.v) {
      Reveal.slide(destination.h, destination.v);
    }
  });
  vm.runInNewContext(source, {
    window: Object.assign(window, { Reveal }), document, Reveal, URL,
    navigator: { userAgent: 'test' }, performance: { now: () => time },
    setInterval: fn => polls.push(fn), setTimeout() { throw Error('unexpected retry'); }
  });
  for (const poll of polls) poll();
  location.hash = '/earlier';
  location.hash = '/latest';
  let delivered = 0;
  while (pending.length && delivered < 100) {
    const event = pending.shift();
    time += 1;
    for (const { handler } of hashHandlers) handler(event);
    delivered += 1;
  }
  assert.equal(pending.length, 0, 'hash event queue did not drain after ' + delivered + ' events');
  assert.equal(current.h, 3);
  assert.equal(current.v, 4);
  assert.equal(location.hash, '#/latest');
  // Expiring the link-protection window must not cause a later jump.
  for (let i = 0; i < 20; i++) {
    time += 60;
    for (const poll of polls) poll();
  }
  assert.equal(current.h, 3);
  assert.equal(current.v, 4);
  assert.equal(pending.length, 0);
});
