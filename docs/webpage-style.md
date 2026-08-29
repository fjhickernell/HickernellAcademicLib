# Shared webpage style guide

This guide is authoritative for reusable webpage conventions in courses,
talks, seminars, workshops, and other `classlib` consumers. Consumer
repositories should document only their audience, terminology, organization,
and intentional local exceptions.

## Organization and headings

- Keep each page focused and cross-link related pages instead of duplicating
  maintained content.
- Use descriptive headings and reasonably short sections for easy scanning.
- Reserve `#` for the page title, normally supplied by Quarto YAML.
- Use `##` for major sections and `###` for genuine subsections. Do not skip
  levels or use headings merely to enlarge text.

## Emphasis and callouts

Use the shared semantic `.key-point` block for an important conclusion:

```markdown
::: {.key-point}
Important idea goes here.
:::
```

Prefer `.key-point` to a generic callout. Use a callout when its type carries
meaning, such as a warning or distinct note. Use either sparingly, and do not
recreate the shared treatment with page-local CSS.

## Mathematics

- Use standard LaTeX supported by Quarto and MathJax.
- Display important equations; keep short secondary expressions inline.
- Define notation when readers first need it and keep it consistent.
- Break long derivations into readable steps with explanatory prose.
- Preserve mathematical accuracy whenever material is converted or condensed.
- Follow the terminology policy in `classlib/AGENTS.md`, including its precise
  use of *stable*, *converges*, *variability*, and *error*.

## Figures

- Preserve useful figures when practical and prefer vector graphics.
- Center figures unless another layout better serves the explanation.
- Add captions when they identify a figure, explain its role, or support a
  useful cross-reference.
- Use descriptive alternative text and meaningful filenames.
- Keep consumer-specific figures local; share genuinely reusable figures.

## Tables

- Use Markdown or Quarto tables rather than screenshots or raw HTML.
- Rely on the shared theme for headers, row differentiation, spacing, and
  alignment rather than reproducing its CSS locally.
- Left-align prose, right-align numeric columns, and center short categorical
  values only when it improves scanning.
- Express alignment in the Markdown separator row when needed:

```markdown
| Item | Description | Value |
|:---|:---|---:|
| Example | Explanatory text | 12.5 |
```

- Restructure overly wide tables rather than forcing difficult scrolling.

## Code and notebooks

- Use inline code for package names, functions, variables, commands, and
  filenames.
- Use fenced blocks with an appropriate language. Use `bash` for terminal
  commands and omit shell prompts so commands remain easy to copy.
- Keep examples focused and omit unrelated setup or output.
- Use executable cells only when execution materially improves the page; make
  dependencies and inputs clear.
- Link to a notebook only after it exists and has been validated. Use
  descriptive link text and show a literal filename only when it matters.

## References and links

- Use bibliography citations where appropriate and avoid raw URLs in prose.
- Use descriptive links that remain meaningful out of context; avoid “click
  here.”
- Cross-reference headings, figures, tables, equations, and pages when doing
  so prevents duplicated explanation.
- Keep links visibly identifiable. Do not override an entire link with an
  emphasis color that hides its affordance.

## Writing and visual consistency

- Write directly, concisely, and completely for the stated audience.
- Introduce specialized terminology before relying on it and use terms
  consistently across pages, slides, notebooks, and assignments.
- Centralize colors, spacing, and typography in shared theme files.
- Use stable semantic classes instead of ad hoc inline styling.
- Preserve clear alignment, predictable list indentation, visible links, and
  enough space for mathematics.
- Design for varied screen sizes rather than one browser or display.

Consumer-local guides may establish audience-specific language, page
organization, semester placeholders, terminology, and exceptions without
duplicating these shared rules.
