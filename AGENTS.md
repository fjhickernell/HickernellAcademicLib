# Shared teaching and presentation resources

## Purpose

`classlib` contains reusable teaching and presentation resources shared across
university courses, conference talks, seminars, workshops, websites, and
future academic projects. These resources include code and styling as well as
shared slides, webpages, and teaching content.

Optimize for reuse, maintainability, stable interfaces, consistency, and clean
abstractions—not one-off implementations.

> Every improvement to `classlib` should make future teaching and presentation
> projects easier to build, not just the current one.

## What belongs here?

Appropriate shared resources include:

- shared SCSS and Reveal.js helpers
- Lua filters, JavaScript utilities, and Quarto extensions
- notebook visualization helpers and reusable Python notebook support
- tree rendering and other reusable visual components
- reusable slide fragments, webpages, teaching content, and website components
- documentation shared across consumers

Content or functionality that benefits only one consumer generally belongs in
that consumer's repository.

## Decision tree

Before implementing a feature, ask:

1. Useful only for one consumer? Keep it in that consumer's repository.
2. Likely to benefit multiple consumers? Develop it in `classlib`.
3. Broadly useful beyond these consumers? Consider an upstream project or
   standalone package.

## Consumer neutrality

Avoid assumptions tied to one consumer, including MATH 332, MATH 565, Fall
2026, a particular conference, or a specific talk. When examples need context,
use neutral placeholders such as `MATHxxx`, `Course Name`, `Talk Title`, or
`Presentation Name`. Parameterize necessary consumer context so shared
resources can be reused without modification.

## Notebook runtime

Use the `qmcpy` Python environment and Jupyter kernel by default for Jupyter
notebooks and Quarto Python execution in courses, conference talks, seminars,
workshops, research projects, websites, and other consumers. This is the
standard runtime even when the consumer does not include QMCSoftware/`qmcpy`
as a submodule. Do not substitute a generic `python3`, `python3.13`, or other
kernel merely because that submodule is absent. Use a different environment
only when the project explicitly requires one.

## Mathematical use of stability terminology

In notebooks, slides, webpages, assignments, and other teaching materials,
reserve **stable**, **stability**, and **stabilize** for situations where
mathematical stability is actually the concept being discussed. Do not use
these words informally merely to say that an estimate changes less as the
sample size increases.

Describe the behavior precisely:

- Use **converges** only when mathematical or statistical convergence toward
  a limiting value is intended.
- Use **sampling variability decreases** when repeated estimates become less
  variable as the sample size increases.
- Use **the estimates concentrate more tightly around ...** when emphasizing
  the distribution of repeated estimates.
- Use **the fluctuations become smaller** for an intuitive description of a
  plot.
- Use **the error decreases** when the plotted or analyzed quantity is the
  error.

Do not mechanically replace **stabilizes** with **converges**. Distinguish
convergence toward a limiting value from decreasing variability around that
value, and state both when both behaviors matter.

## Shared slides and webpages

Write reusable content for its medium:

- Shared slides prompt spoken explanation; they are not prose documents
- Prefer concise, information-dense phrases; remove words that add rhythm but
  little meaning
- Prefer fragments and compact clauses when clear; do not force every bullet
  into a grammatical sentence
- Omit terminal periods and prose-list punctuation unless needed for clarity
- Use complete sentences when precision requires them, including definitions,
  policies, quotations, warnings, and carefully worded conclusions
- Prefer `[key concept]{.alert}` over Markdown bold (`**key concept**`) for
  emphasis in slides
- Keep text links visibly identifiable as links. Do not apply `.alert` or
  another color override to an entire text link; put that emphasis beside the
  link or on only part of a longer linked phrase
- Nested semantic styling may override part of a link when surrounding linked
  text still carries the link styling. For example,
  `[Companion \`NotebookName\` notebook](...)` may preserve inline-code styling
  on the notebook name because the surrounding linked words identify the
  whole phrase as a link. If the whole label would be inline code or another
  override, add descriptive linked text or otherwise preserve a visible link
  cue
- Prefer `\implies` over `\Rightarrow` for mathematical implication
- Shared webpages may use fuller prose because readers must follow them without
  a speaker
- Preserve mathematical and conceptual precision in both media
- Keep slides visually clean; preserve useful figures when practical
- Use progressive disclosure only when it improves understanding
- Prefer shared semantic CSS classes and reusable components over inline or
  consumer-local styling
- When two adjacent content columns need a deliberate visual gutter, use the
  **Pomona gutter**: two 47% content columns separated by an empty 6% column.
  Prefer this readable Quarto structure over one-off CSS for an isolated slide
- Avoid consumer-specific assumptions unless explicitly parameterized

Teaching decks and research talks may need different presentation profiles;
encode genuinely reusable differences as shared, consumer-neutral variants.
Keep event identity, deck structure, and one-off scientific layouts local.

For example, prefer `Three possible outcomes: no solution, one solution,
infinitely many solutions`, `Row operations preserve the solution set`, and
`Compute to explore; reason to justify` over fuller prose that supplies spoken
transitions.

Detailed shared style rules should eventually live in one authoritative
`classlib` guide for each medium, with profiles where teaching and research
presentations genuinely differ. Consumer repositories should reference those
guides and document only local exceptions. Until a rule is deliberately
migrated, its current consumer guide remains authoritative for that consumer.

## Consumer repository pattern

Every new course, conference talk, seminar, workshop, website, or other
consumer must follow the authoritative [consumer-adoption
contract](docs/consumer-adoption.md). Use its bootstrap tool so the pinned
submodule and root `AGENTS.md` make this shared guidance discoverable without
copying it locally.

## API stability and backward compatibility

Treat documented CSS class names, shortcode syntax, Lua filter arguments, YAML
schemas, JavaScript interfaces, include paths, parameterized content
interfaces, and file layouts as stable public APIs whenever practical.

- Preserve existing behavior
- Extend rather than replace
- Document intentional breaking changes
- Provide migration notes when appropriate

## Reuse before duplication

Before creating code, styling, or content, look for an existing shared resource
or similar implementation. Prefer extending a sound abstraction, and consider
whether the result can serve a more general need. Avoid parallel
implementations of the same capability.

## Testing

Before committing reusable resources:

- Run focused automated tests when available
- Render representative examples
- Verify at least one consuming repository still works
- Check the browser console when relevant
- Run `git diff --check`

Scale validation to the interface and consumers affected by the change.

## Documentation

Each reusable capability or content family should have one authoritative
description, one representative example, intended usage, and migration notes
when behavior changes. Reference that source elsewhere instead of duplicating
it.

## Design philosophy

Optimize for simplicity, readability, maintainability, reuse, and consistency.
Avoid clever solutions that increase long-term maintenance cost.

Operational workflow is governed by the global
`SharedConfigs/codex/AGENTS.md` instructions. This document explains how
shared teaching and presentation resources should evolve.
