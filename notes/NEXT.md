# NEXT

## Current focus

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
