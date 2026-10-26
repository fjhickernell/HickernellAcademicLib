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
