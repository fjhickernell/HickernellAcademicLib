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

## Development and canonical checkouts

Keep one ordinary editable clone on each development computer:

```bash
cd ~/SoftwareRepositories/HickernellAcademicLib
git status
git pull --ff-only
```

Inspect the worktree before pulling or editing. Do not overwrite or discard
uncommitted work from another session.

When a reusable change must be seen or exercised in a real course, talk, or
other project, prototype it inside that active consumer repository's pinned
`classlib/` checkout and validate it immediately with the consumer's actual
slides, website, notebooks, or build. If no consumer is specified, ask which
active consumer to use when the choice matters; otherwise choose a suitable
repository currently under construction, preferring the current repository
when it is representative.

Do not publish a divergent shared change from a consumer submodule. Once the
prototype is validated in context, transfer it to the canonical clone, perform
the appropriate canonical and representative-consumer validation, and commit
and push it there. Then update each intended consumer to the resulting exact
commit.

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

The authoritative [consumer-adoption contract](docs/consumer-adoption.md)
defines how every durable consumer initializes, discovers, audits, and
intentionally updates its pinned `classlib` dependency. Use its bootstrap for
new repositories and its read-only check during normal consumer validation.

The consumer's own instructions still define the policy for other
dependencies; do not assume they follow the `classlib` model.

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

Follow the intentional pointer-update procedure in the [consumer-adoption
contract](docs/consumer-adoption.md). Publishing the library never advances a
consumer automatically.

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

- choose an active consumer that provides a representative development and
  validation context;
- inspect the consumer and its pinned `classlib/` checkout before editing;
- prototype the reusable change in that checkout and validate the consumer;
- inspect and synchronize the canonical clone without discarding local work;
- transfer the validated reusable change to the canonical clone;
- confirm that the proposed change is reusable;
- check other relevant consumer repositories for pre-existing work.

Before updating a consumer:

- publish and identify the validated library commit;
- inspect the consumer repository and all relevant submodules;
- check out the exact library commit in `classlib/`;
- run the consumer-bootstrap check;
- validate the consumer;
- commit only the intentional submodule-pointer change.

This model gives every consumer stable inputs while allowing
`HickernellAcademicLib` to evolve as one shared academic library.
