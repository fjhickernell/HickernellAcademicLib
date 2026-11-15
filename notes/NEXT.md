# NEXT

## Current focus

The academic website now links to the November 16 StrategicSamplingColloquium talk on Talks and Featured Resources. Its title-slide QR points to this academic homepage. Later talk deployments update the linked destination without copying slides into the library.

The reusable collaborator workflow is documented in `docs/collaborators.md`
and routed from `AGENTS.md`. Master names/IDs stay in the names-only catalog;
master photographs stay in iCloud Drive’s `Collaborator Headshots` archive.
`tools/collaborator_assets.py` and its shell launcher refresh explicit
consumer selections and check publishing copies without iCloud access.
Samuel Vangu is added to the master names catalog. Nine focused tests pass;
StrategicSamplingColloquium is the selected integration consumer. The shared
changes are validated in its consuming checkout. This Checkpoint publishes
the canonical library before advancing that consumer pin; other consumers
retain their intentional pins.

The automatic table-index default is documented in `AGENTS.md`: omit display
row numbers unless they carry a clearly labeled meaning or support a specific
explanation. Preserve meaningful run, seed, iteration and similar data columns.
The MATH 565 SGD notebook validates this convention in its saved tables.
MATH 565 is the selected consumer for this documentation-only update; other
consumers retain their intentional pins.

Every student-action course deadline now belongs on the course Schedule as
well as its detailed page, with linked instructions and coordinated date
changes. The rule is documented in `AGENTS.md` and exercised by MATH 565's
presenter and observer sign-up entries. MATH 332 and MATH 565 are the selected
consumers for this guidance update; other consumers retain their intentional
pins. No runtime behavior changes.

The simple-fraction preference is documented in `AGENTS.md`: use slash
notation in running text and stacked fractions in displayed equations.
MATH 332 is the selected consumer for this documentation-only update; other
consumers retain their intentional pins. No runtime behavior changes.

The all-course grading-tracker progress default is documented in `AGENTS.md`.
MATH 565 is the selected consumer for this guidance update; other consumers
retain their intentional pins. The global instructions route future tracker
preparation to this default. No further implementation is needed.

The queued-hash slide-navigation fix is validated in MATH 332 and transferred
to the canonical checkout. Resolve current URL targets rather than replay stale
hash events, and protect a direct child target when Reveal handles the URL
before the helper. All five Node regressions pass. In the real-browser queued
navigation fixture, the original code loops until the 43-event safety cutoff;
the fix settles on the requested child after two events. Ordinary arrows,
section links and browser back/forward retain their intended behavior.

The reusable implementation and regression are complete. MATH 332 is the
selected consumer for this exact update; publish the canonical library before
advancing its pin. Course issue 3 records the deployment and reporter closeout.
Other consumers retain their intentional pins.

The local MathJax runtime fix is complete and validated in MATH 332.
Safari stalled loading the external CDN script, leaving raw TeX after reloads.
The shared configuration and loader fallback now serve bundled MathJax 3.2.2
with license and provenance. Twelve consumer decks render; Safari reload and
slide/section navigation pass, confirmed by the instructor. The canonical change is
published as `8b84f9a` and adopted by MATH 332. Other consumers retain their
pins until deliberately selected for adoption.

The responsive footer fix is complete and validated in the MATH 332 consumer.
Shared footer text scales with viewport width and reserves menu-button space.
All eleven consumer decks render cleanly; complete footers were checked at
1280 by 720, with additional 1600 by 1000 and 1024 by 768 checks. The SCSS and
slide-style guidance match the validated consumer prototype.

The named-deck reference convention and delayed-loader validation remain
complete. No additional shared implementation task is selected. Preserve
consumer-neutral guidance and use exact published commits for intentional
consumer updates; do not advance unrelated consumers automatically.

When working in a consuming repository, always ask:

- Is this reusable?
- Does it belong in `classlib` instead?

If yes:

1. Implement here.
2. Validate here.
3. Publish here.
4. Update consuming repositories.

## Candidate improvements

- Further consolidate shared SCSS
- Expand reusable Reveal.js components
- Generalize notebook visualization helpers
- Improve the tree-marker framework
- Reduce duplicated Quarto templates
- Improve documentation and examples
- Audit shared APIs for consistency

## Questions to resolve

- Which consumer-specific utilities or content should migrate into `classlib`?
- Are additional shared slide fragments warranted?
- Which repeated inline layouts in research talks warrant shared semantic
  components rather than local styling?
