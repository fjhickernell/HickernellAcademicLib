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

## Development checkout

Prototype and validate a reusable `classlib` change inside the pinned
`classlib/` checkout of an active consumer repository whenever the change
needs to be seen or exercised in that consumer's actual slides, website,
notebooks, or build. This keeps the shared source and its representative use
together during development and makes visual and integration review immediate.

If the user does not name a consumer, ask which active consumer to use when
the choice could materially affect the result. Otherwise, choose a suitable
active repository currently under construction, preferring the current
repository when it provides a representative validation context. Do not use
an older or reference-only consumer for development without explicit
authorization.

Treat work in a consumer's `classlib/` checkout as an uncommitted prototype.
After it is validated in context, transfer the reusable change to the
authoritative `HickernellAcademicLib` checkout, validate it there as
appropriate, commit and push it upstream, and then intentionally update the
consumer's pinned submodule commit. Do not commit a divergent shared change
only inside a consumer submodule.

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

## Heading hierarchy

Normally, a section or subsection that introduces another heading level
should contain at least two child sections or subsections at that level. When
there is only one child, fold it into the parent or remove the unnecessary
heading level. A singleton child is acceptable when it is a deliberate special
case and the additional hierarchy materially clarifies the structure; treat
that as an exception rather than the default.

## Shared slides and webpages

Before substantial slide work, read the authoritative
[`docs/slide-style.md`](docs/slide-style.md). Before substantial webpage work,
read the authoritative
[`docs/webpage-style.md`](docs/webpage-style.md). For diagrams and specialized
RevealJS layouts, also follow
[`docs/revealjs-diagram-construction.md`](docs/revealjs-diagram-construction.md).

The guides define the shared teaching baseline. Encode genuinely reusable
differences, such as a research-presentation profile, as consumer-neutral
variants. Keep event identity, deck sequence, course terminology, local
notation, one-off scientific layouts, and explicit exceptions in the
consumer. Consumer guides should link to the shared source and avoid copying
its universal rules.

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
