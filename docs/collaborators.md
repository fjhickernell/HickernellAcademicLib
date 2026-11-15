# Collaborators and headshots

Use this workflow for future talks and intentional updates of existing talks.
Fred selected the master-list/iCloud arrangement and crop-only preparation on
November 15, 2026. It is the shared default, not a default list of people.

## Authoritative sources

- Names and stable IDs: `classlib/quarto/metadata/hickernell-collaborators.yml`
  in HickernellAcademicLib. Keep this catalog names-only; do not infer roles,
  contact details, authorship, or permission from membership.
- Master photographs: iCloud Drive's `Collaborator Headshots` folder, normally
  `~/Library/Mobile Documents/com~apple~CloudDocs/Collaborator Headshots`.
  Its `catalog.yml` records ready-to-use filenames, source provenance and
  SHA-256 hashes. Originals and preparation tools stay in that archive.
- Talk selection and order: an explicit consumer file, normally
  `data/collaborators.yml`. Adding a master-catalog entry must never add a
  person to a talk automatically. Apply the author's intended ordering;
  a surname-ordered gallery should be checked in visual reading order too.

Keep master photos in iCloud. A public talk repository retains only the
selected publishing copies, a small manifest, and generated gallery includes
needed for a reproducible build. Public CI reads those copies and the pinned
name catalog; it does not need iCloud access or a public iCloud sharing link.
Existing historical source assets need not be bulk-migrated during adoption.

## Add or prepare a person

1. Check the master catalog for an existing person; preserve that stable ID.
   New IDs follow the existing surname-first slug convention. Obtain the
   author's intended display name rather than guessing from an account name.
2. Retain the acquired original in the archive, with its source URL or supplied
   file provenance. Record the intended use and any supplied permission
   accurately; do not invent blanket reuse permission.
3. Use the archive's `tools/prepare-headshot.py` and `docs/Trimming.md` for
   deterministic crop/resize. Fred's default is crop-only, with no AI facial
   editing. Preserve the original, review the candidate, and record its crop
   box and output hash. Prefer a versioned filename to overwriting an
   established master portrait.
4. Add the ready-to-use file and its metadata to the iCloud `catalog.yml`.
   Add the name/ID to the shared names catalog when new. Follow the normal
   canonical-library publication-before-consumer-pin workflow.
5. Explicitly add the ID to the selected talk. For unusual acknowledgments,
   preserve the author's role/description separately from the names catalog.

## Select and refresh a talk

Example consumer selection:

```yaml
schema_version: 1
photo_directory: assets/headshots/processed
manifest: assets/headshots/manifest.json
extra_ids: [kuo-frances] # Used by a custom layout, not this gallery
galleries:
  collaborators:
    output: slides/_includes/collaborators.qmd
    image_prefix: ../assets/headshots/processed
    portrait_width: 135
    columns: 6
    ids: [choi-sou-cheng, ding-yuhan]
```

From the consumer root, in an environment with PyYAML (included in the
library's dependencies):

```sh
bash classlib/tools/collaborator_assets.sh data/collaborators.yml --refresh
bash classlib/tools/collaborator_assets.sh data/collaborators.yml --check
```

The shell launcher reuses the standard local `qmcpy` interpreter, falling
back to `python3` on other hosts. Set `COLLABORATOR_PYTHON` to an existing
interpreter/CI virtual environment when needed. It installs nothing. The Python
script can also be called directly from an activated environment with PyYAML.

Use `--photo-root PATH` or `HICKERNELL_HEADSHOT_DIR` when the archive is in
another local iCloud location. Check directory availability and file hashes
on the current Mac; local availability does not prove delivery to other Macs.
Refresh validates all selected source files before writing publishing copies.
It never modifies the archive or deletes unselected assets. Check is read-only
and detects missing/modified copies, changed master names and stale includes.

Include the generated QMD in the slide. Omit `columns` to generate cards only
inside a consumer-owned grid. A text block can span several columns in that
same grid so portrait columns remain aligned across rows. Custom prose may
read names via Quarto metadata after loading the master names YAML. For a
custom portrait layout, also load the generated JSON manifest so a versioned
photo filename can change without editing the slide:

```yaml
metadata-files:
  - ../classlib/classlib/quarto/metadata/hickernell-collaborators.yml
  - ../assets/headshots/manifest.json
```

Use `collaborators.<id>.name` for the authoritative display name and
`headshots.<id>.file` for the selected publishing filename. For example:

```html
<img src="../assets/headshots/processed/{{< meta headshots.kuo-frances.file >}}"
     alt="{{< meta collaborators.kuo-frances.name >}}">
```

Run `--check` before rendering and in CI. A Quarto project pre-render script
can call it; [Quarto runs project scripts from the project directory](https://quarto.org/docs/projects/scripts.html).
Install PyYAML in CI before that check. Render and visually inspect the actual
slide at the usual presentation size, including ordering, captions, crop,
column alignment, duplicate people, footer clearance and image loading.

Keep this document authoritative. Consumer notes record the chosen people,
layout and remaining local work; they link here rather than duplicating the
workflow. The iCloud archive holds photo-specific acquisition and crop records.
