# Shared slide style guide

This guide is authoritative for reusable RevealJS conventions in `classlib`
consumers. It provides the teaching-deck baseline; research talks may define a
shared profile where their needs genuinely differ. Consumer repositories
should record only deck structure, terminology, notation, local components,
and intentional exceptions.

For specialized diagrams, also follow
[`revealjs-diagram-construction.md`](revealjs-diagram-construction.md).

## Slide writing

- Slides prompt spoken explanation; they are not prose documents.
- Write punch points: short phrases, compact clauses, and equations that the
  audience can scan while listening. Avoid paragraph-shaped exposition and
  sequences of complete explanatory sentences.
- Omit terminal periods. Use complete sentences only when precision genuinely
  requires them, as in definitions, policies, quotations, or warnings.
- Preserve mathematical precision while removing words that add little
  information.
- Prefer `[key concept]{.alert}` to Markdown bold for short emphasis.
- Keep links visibly identifiable; do not color an entire link as an alert.
- Prefer `\implies` to `\Rightarrow` for mathematical implication.
- Use progressive disclosure only when it improves understanding.

## RevealJS heading structure

- Use `#` for a major section and `##` for an individual slide.
- Use `###` within a `##` slide only for a real third-level heading; use
  `####` only for genuinely subordinate labels.
- Do not place `###` directly after `#`; begin the individual slide with `##`.
- Use raw `<h3>` or `.h3` for heading-like styling without hierarchy changes.
- Use title case for `#` headings and sentence case for `##` and `###`, apart
  from proper nouns, acronyms, and mathematical notation.

## Teaching-deck navigation

A teaching deck should show its place in the larger sequence and its internal
structure. The standard opening pattern is:

1. A generated title slide identifying the course or presentation and deck.
2. A Course Map or comparable overview showing the larger sequence and the
   current deck's major sections.
3. Instructional sections in presentation order.

When using section-outline slides:

- Repeat each linked `#` heading exactly in the overview.
- List subordinate `##` slides on the section slide in presentation order;
  omit `###` subheadings.
- Update outlines whenever slides are added, removed, renamed, or reordered.
- Put brief framing above links and examples or figures below them. Move dense
  content to its own `##` slide.

Consumer metadata should define deck titles and previous/next navigation. Keep
sequence length, textbook coverage, footer labels, cumulative indexes, and
other course architecture local.

## Shared theme and semantic classes

Use `hickernell-slides.scss` before adding local CSS. Add consumer-wide CSS
only for conventions shared by that consumer and deck-specific CSS only for a
genuine one-deck exception.

Shared features include:

- a consistent content rail and projector-safe heading banners;
- coordinated title, footer, slide-number, control, and navigation styling;
- `.headerless` to suppress a banner and `.hidden` to hide an element;
- `data-state="goldborder"` for the standard gold border;
- `.key-point`, `.main-message`, and `.alert` for semantic emphasis;
- `.h3`, `.small`, `.indent`, `.hanging`, `.refs`, and `.ref-label`;
- `.flexline`, `.pushright`, `.line-right`, and `.right` for established line
  layouts;
- `.vspace-sm`, `.vspace`, `.vspace-lg`, and `.text-end` for standard spacing
  and alignment.

Use these classes according to meaning, not incidental appearance.

## Columns and layout

- Prefer shared semantic components to inline or consumer-local styling.
- For two adjacent ideas, use the Pomona gutter by default: 47% content, 6%
  empty gutter, and 47% content. Adjust when content balance requires it.
- Use explicit grid placement for specialized diagrams and follow the shared
  diagram guide's accessibility and visual-inspection rules.
- Position an overlay element itself rather than changing RevealJS's slide
  positioning model.

## Tables and bullets

- Use Markdown tables and rely on the shared theme for projector-friendly
  headers, rules, padding, and row differentiation.
- Unordered lists use en-dashes by default. Use `.dash-bullets` or
  `.circle-bullets` when that choice fits the slide.
- Preserve distinct nested markers and shared indentation.

## Exercises

Use `.exitem` with `$\exstar$` so multiline exercise text aligns reliably:

```markdown
::: {.exitem}
<span class="exbullet">$\exstar$</span>
<span>
Exercise description goes here and may wrap across lines.

<span class="exsub">Indented follow-up line.</span>
</span>
:::
```

Do not put a Markdown list inside `.exitem`. Use `<p>` for multiple paragraphs
and `.exsub` for indented follow-up lines.

## Key points

Use `.key-point` rather than a generic callout for an important conclusion:

```markdown
::: {.key-point}
Important idea goes here.
:::
```

When a `.key-point` contains two or more distinct statements, put each
statement in its own paragraph so that the ideas read separately. Insert a
standalone `&nbsp;` paragraph between them when at least one statement is long
enough to occupy roughly two-thirds of a line or to wrap at the standard slide
viewport. Omit the spacer when the statements are shorter, because the extra
empty space weakens rather than clarifies the grouping. Treat this as a visual
heuristic, not a source-text character count.

Reserve `.main-message` for a stronger central takeaway.

## Mathematics and shared macros

- Prefer displayed equations, avoid overcrowding, and preserve accuracy.
- Use parentheses for function evaluation. Use ordinary parentheses for
  simple arguments and matched scalable parentheses such as
  $f\bigl(g(x)\bigr)$ for nested or visually tall arguments. Reserve curly
  braces for notation in which they carry mathematical meaning, including
  sets, events, sample sets, and alternatives in expressions such as
  $\min\{1,\ldots\}$. Established probability and expectation operator
  grouping may retain its existing convention.
- Write **low discrepancy** without a hyphen, including in *low discrepancy
  sequence* and *randomized low discrepancy estimator*.
- Check `hickernell-latex-macros.js` before spelling out notation. Use an
  existing semantic macro whenever its meaning matches.
- Prefer macros such as `\Bern`, `\Bin`, `\Unif`, `\Norm`, `\Exp`, `\Gam`,
  `\Pois`, `\Prob`, `\Ex`, `\var`, `\cov`, `\reals`, and `\dif` rather than
  duplicating their expansions.
- Use `\varrho` for probability mass and density functions and reserve `\rho`
  for correlation or other meanings.
- Use `gather*` for successive displays, `align*` for shared alignment points,
  and `multline` for one long equation that must wrap.
- Propose a shared macro for recurring shared notation, not merely to shorten
  a one-off expression. Keep JavaScript and TeX definitions aligned when both
  outputs require it.
- Render mathematical plot labels in a serif math font consistent with the
  displayed mathematics.

Consumer-local guides should state indexing and specialized notation choices.

## Figures and sourced images

- Preserve useful figures, prefer vector graphics, and center them unless
  another placement serves the explanation.
- Use descriptive alternative text and meaningful filenames.
- For a sourced image, link the image and add `.image-source` to the link:

```markdown
[![](assets/images/example.jpg){fig-alt="Concise image description"}](https://example.com/original){.image-source target="_blank" rel="noopener" style="width: 95%;" title="View image source"}
```

Put display width on the link, use `fig-alt` for non-visible alternative text,
and retain `target="_blank" rel="noopener"` for external sources.

## References and metadata

- Load recurring books and papers from shared metadata when available rather
  than repeating citation text or publisher URLs.
- Use bibliography citations and metadata shortcodes; avoid raw URLs.
- Keep event identity, course-specific references, deck structure, local
  marker presets, and one-off scientific layouts in the consumer.

## Validation

Render every affected representative deck, inspect it at its standard
viewport, verify navigation and internal links, and check the browser console
when relevant. Validate a shared change in at least one real consumer and in
each consumer whose local conventions changed.
