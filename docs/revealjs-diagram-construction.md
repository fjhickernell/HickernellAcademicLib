# RevealJS diagram construction

Use the simplest representation that keeps the visual precise, accessible,
maintainable, and easy to validate in a real consumer deck.

## Choose the representation deliberately

- Use ordinary Quarto Markdown for prose, equations, columns, and lists.
- Use semantic HTML with scoped CSS Grid or Flexbox for text-heavy diagrams,
  timelines, process layouts, and visuals whose labels should remain real HTML
  text. The shared computing-technology timeline uses semantic HTML and CSS
  Grid for its milestones.
- Use inline SVG for geometric drawings, coordinate plots, arrows, paths, or
  other visuals whose relationships are easiest to express in one coordinate
  system. The computing-technology timeline uses one decorative inline SVG
  for its continuous, multicolor serpentine connector.
- Use a raster image for photographs and for visuals whose source medium is a
  bitmap. Do not redraw a photograph or movie image as SVG.
- Do not combine representations merely for novelty. A decorative SVG path
  behind semantic HTML labels can be appropriate, but the layering and
  alignment must remain explicit.

## Make placement deterministic

- When a CSS Grid diagram depends on a particular position, set both
  `grid-row` and `grid-column` explicitly. Do not rely on auto-placement for a
  timeline, matrix-like comparison, or other semantically ordered diagram.
- Anchor timeline markers and connectors to fixed grid coordinates or a shared
  path. Do not let varying label height determine marker position. Center each
  marker on the visible stroke, accounting for stroke width rather than only
  the path or border coordinate.
- Keep connectors behind nodes and labels. Scope every diagram selector with a
  distinctive component prefix so an included fragment cannot alter another
  slide.
- Give each connector one authoritative drawing mechanism. Do not overlay a
  CSS border and an SVG path for the same segment; duplicated geometry can
  render as a double line after RevealJS scaling.
- For a multicolor rounded turn, prefer one continuous path with a gradient or
  another explicit transition over differently colored CSS borders meeting
  inside a radius.
- Separate chronology from source order when a serpentine timeline reverses
  direction. Preserve accessible reading order in the markup and state the
  overall sequence in an `aria-label` when the visual order is non-linear.
- Use both sides of a path only when the distinction is meaningful and
  consistent, such as hardware on one side and software on the other.

## Shared fragments and assets

- Keep a reusable fragment consumer-neutral and include a `[Sources]` block in
  its speaker notes for non-trivial claims and external assets.
- Provide alt text for informative images and a useful `role` or `aria-label`
  for the complete diagram.
- Test asset paths through the consumer's actual Quarto preview or render. A
  generic static-file server may resolve an included fragment's relative paths
  differently and can produce a false missing-asset failure.
- Keep copyrighted promotional artwork out of reusable shared assets unless
  its use and redistribution rights have been intentionally reviewed. Prefer
  an authoritative public-domain or suitably licensed image when it serves the
  same teaching purpose.

## Render and inspect

After every material diagram change:

1. Render the representative consumer deck at its standard RevealJS size.
2. Inspect the complete slide at full size and at an ordinary scaled browser
   viewport.
3. Check title and footer clearance, text wrapping, marker alignment,
   connector continuity, image crops, and every intentionally adjacent label.
4. Inspect the browser console when scripts or interactive behavior are
   involved.
5. For programmatic layouts, compare element bounding boxes or otherwise check
   that no label extends into the next annotation, note, or footer.
6. Run `git diff --check` and keep rendered output out of Git.

Do not accept a diagram merely because it renders without an error. Visual
inspection in the actual consumer is part of validation.
