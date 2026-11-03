# NEXT

## Current focus

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

The slide navigation correction is validated in MATH 332: cross-section links
to continuation headings, direct hash addresses, and initial deep links retain
their requested slide; horizontal arrows still start at the section overview.
Four Node regression tests cover these behaviors and run before website
publication. MATH 332 is the selected consumer for this exact library update;
other consumers retain their existing pins.

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
