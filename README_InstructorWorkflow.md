# Instructor Workflow for HickernellAcademicLib

This document describes how to develop and use **HickernellAcademicLib**
across multiple computers and multiple consumer repositories, including
courses, conference talks, seminars, workshops, websites, and other academic
projects.

The workflow has two goals:

- maintain one canonical, reusable academic library;
- let each consumer repository use an intentional, reproducible library
  version.

## Repository roles

`HickernellAcademicLib` is the canonical source repository. It contains
reusable code, Quarto styling, metadata, snippets, notebooks, slide fragments,
webpages, teaching content, and presentation components useful to more than one
consumer.

A consumer repository normally mounts this repository at `classlib/` as a Git
submodule. Consumer repositories contain their own project-specific content,
configuration, navigation, schedules or event details, and assets.

Before moving a change into `HickernellAcademicLib`, ask whether it is
genuinely reusable. Keep consumer-specific content and local presentation
adjustments in the consumer repository.

## Canonical checkout

Keep one ordinary editable clone on each development computer:

```bash
cd ~/SoftwareRepositories/HickernellAcademicLib
git status
git pull --ff-only
```

Inspect the worktree before pulling or editing. Do not overwrite or discard
uncommitted work from another session.

Develop reusable changes in this canonical clone, not inside a consumer
repository's `classlib/` checkout. Validate the library change in the canonical
clone and in representative consumers when appropriate.

## Editable installation

Install the canonical clone into the Python environment used for development:

```bash
cd ~/SoftwareRepositories/HickernellAcademicLib
python -m pip install -e .
```

Activate the appropriate virtual or Conda environment first when one is used.
An editable installation makes `import classlib` resolve to the canonical
development clone while consumer repositories retain pinned submodule
versions for reproducible builds.

After switching computers or environments, verify where Python imports the
package from:

```bash
python -c "import classlib; print(classlib.__file__)"
```

## Consumer repositories

After cloning or pulling a consumer repository, initialize the exact submodule
commits recorded by that repository:

```bash
git submodule update --init --recursive
```

Routine setup and builds must use these recorded commits. Do not use
`git submodule update --remote` as a routine synchronization command, because
it replaces a reproducible pinned version with a moving branch tip.

The consumer repository's own `AGENTS.md`, workflow documentation, and
`.gitmodules` define which submodules are writable and how they may be
updated. Do not assume that other dependencies follow the same policy as
`classlib`.

## Publishing a reusable library change

In the canonical clone:

```bash
cd ~/SoftwareRepositories/HickernellAcademicLib
git status
git add <files>
git commit -m "<describe the reusable change>"
git push
```

Run the validation appropriate to the change before publishing it. Commit only
the intended reusable work.

Publishing the library does not automatically update any consumer. Each
consumer remains pinned until its submodule pointer is deliberately advanced.

## Updating a consumer's pinned `classlib` version

First publish and identify the validated `HickernellAcademicLib` commit. Then,
in the consumer repository:

```bash
git submodule update --init --recursive
git -C classlib fetch origin
git -C classlib checkout <validated-commit>
```

Validate the consumer with that exact commit. If the result is correct, record
the new pointer in the consumer repository:

```bash
git add classlib
git commit -m "Update classlib to <short-commit>"
git push
```

Advancing the pointer is an intentional consumer change. Do not advance it
merely because a newer library commit exists, and do not include unrelated
submodule changes.

## Working across computers

On the computer where reusable work is created, validate, commit, and push it
from the canonical `HickernellAcademicLib` clone.

On another computer, inspect the canonical clone and synchronize it before
continuing:

```bash
cd ~/SoftwareRepositories/HickernellAcademicLib
git status
git pull --ff-only
python -m pip install -e .
```

Consumer repositories synchronize independently. Pull the consumer and restore
its recorded submodule state:

```bash
git pull --ff-only
git submodule update --init --recursive
```

This keeps reusable development synchronized while preserving each course or
talk as a reproducible snapshot.

## Checklist

Before reusable library work:

- inspect the canonical clone's branch, status, and recent commits;
- synchronize without discarding local changes;
- confirm that the proposed change is reusable;
- check relevant consumer repositories for pre-existing work.

Before updating a consumer:

- publish and identify the validated library commit;
- inspect the consumer repository and all relevant submodules;
- check out the exact library commit in `classlib/`;
- validate the consumer;
- commit only the intentional submodule-pointer change.

This model gives every consumer stable inputs while allowing
`HickernellAcademicLib` to evolve as one shared academic library.
