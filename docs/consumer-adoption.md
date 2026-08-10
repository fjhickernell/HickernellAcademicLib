# Adopting classlib in a consumer repository

Courses, conference talks, seminars, workshops, websites, and other academic
projects are durable consumers of `classlib`. Each consumer records an exact
library version so its materials remain reproducible while shared guidance and
infrastructure continue to evolve.

This bootstrap is the standard for new consumers. Do not retrofit an existing
consumer merely for conformity; an active consumer may adopt it later as an
intentional repository change.

## Consumer contract

Every new consumer must:

1. Mount HickernellAcademicLib at `classlib/` as a pinned Git submodule.
2. Initialize the commit recorded by the consumer before substantive work.
3. Keep the managed shared-guidance contract in its root `AGENTS.md`.
4. Apply guidance in this order:
   1. applicable global instructions;
   2. shared guidance in the pinned `classlib/AGENTS.md`;
   3. consumer-local instructions and explicit local exceptions.

The root contract makes the shared guidance discoverable; it is not a local
copy of that guidance. Universal teaching, presentation, webpage, component,
and infrastructure rules belong in `classlib`. A consumer keeps only its own
identity, content, navigation, terminology, notation, validation requirements,
assets, event or semester details, and other project-specific rules locally.

## Local exceptions

A consumer may override a shared rule when its needs genuinely differ. Record
the override under an `Explicit local exceptions` heading in the consumer's
root `AGENTS.md` or a local guide that `AGENTS.md` names. State the shared rule
being overridden, the replacement behavior, its scope, and the reason.

Do not describe an accidental inconsistency as an exception. Flag an apparent
conflict for review rather than silently choosing one version or copying the
shared rule locally.

## Initialize a new consumer

Run the bootstrap from a canonical HickernellAcademicLib checkout:

```bash
python tools/bootstrap_consumer.py init /path/to/consumer
```

By default, the command adds the canonical SSH submodule URL. Use
`--classlib-url` when the consumer needs another valid URL:

```bash
python tools/bootstrap_consumer.py init /path/to/consumer \
  --classlib-url https://github.com/fjhickernell/HickernellAcademicLib.git
```

The command verifies the repository, adds or initializes `classlib/`, and
installs the canonical managed block in root `AGENTS.md`. It does not impose a
course, talk, website, Quarto, or other project structure. It does not commit
or push. Git stages `.gitmodules` and the gitlink when adding a submodule; the
bootstrap leaves that ordinary Git state for review. Repeating it is safe.

If the consumer already records `classlib`, `init` verifies that relationship.
It never fetches a newer library version or changes the recorded pointer. A
different initialized checkout or malformed existing contract stops the
operation for manual review.

## Audit a consumer

From the consumer root, use the bootstrap version pinned by that consumer:

```bash
python classlib/tools/bootstrap_consumer.py check .
```

The canonical checkout may instead check an explicitly named repository when
testing it against the latest bootstrap contract.

The check is read-only. It verifies:

- `.gitmodules` records `classlib` at the `classlib/` path with a URL;
- the parent repository tracks `classlib` as a gitlink;
- the submodule is initialized at the recorded commit;
- the pinned library contains `classlib/AGENTS.md`;
- root `AGENTS.md` contains the intact canonical consumer contract.

Run this check during initialization and normal checkpoint validation. Add it
to existing CI when automated validation is appropriate for that consumer.
Whether a repository warrants CI depends on its validation and maintenance
needs, not on whether it is a course, talk, seminar, workshop, or website.

## Update the pinned library version

Publish and identify a validated HickernellAcademicLib commit first. Then, in
the consumer repository:

```bash
git submodule update --init --recursive
git -C classlib fetch origin
git -C classlib checkout <validated-commit>
git add classlib
python classlib/tools/bootstrap_consumer.py init .
python classlib/tools/bootstrap_consumer.py check .
```

Validate the complete consumer with that exact commit before recording the
new gitlink in a commit. Staging the gitlink before running the bootstrap makes
the intended commit explicit; it does not publish the change. If validation
fails, correct the problem or restore the previously recorded pointer.
Advancing the pointer is an intentional consumer change. Never advance it
merely because a newer commit exists, and never combine it with an unrelated
dependency update.
