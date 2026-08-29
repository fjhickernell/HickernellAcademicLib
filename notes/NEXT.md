# NEXT

## Current focus

No active shared-resource task.

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
