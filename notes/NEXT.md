# NEXT

## Current focus

The MATH 332 consumer has validated the named-deck reference convention in
`docs/slide-style.md`, including its eleven-deck course maps and split
Chapter 4 material. Mathematical typesetting and footer symbols now pass
visible review in that consumer; the earlier delayed-loader check is complete.
No new shared implementation task is selected. Preserve the consumer-neutral
guidance and consider the candidate improvements below when requested.

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
