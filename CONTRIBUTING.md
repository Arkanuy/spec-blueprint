# Contributing

This repo is a set of empty documents for other people to fill in. The rules are simple.

---

## Folder map

| Folder | Contents | May it contain examples? |
|---|---|---|
| `docs/**` | Documents copied into the user's project | **No.** Must stay empty and ready to fill |
| `AGENT-RULES.md` | The agent contract for the user's project | No |
| `scripts/` | Tooling, not documentation | – |
| Repo root (`README.md`, `CONTRIBUTING.md`) | Documentation for this repo | – |

---

## Rules we hold to

1. **No examples inside the documents.** If a section is hard to understand, fix its heading or its
   guiding question — do not add an example. Examples make people copy instead of think.
2. **No decorative columns.** Every section must prevent one real kind of mistake. If you cannot name
   the mistake it prevents, delete the section.
3. **No `{{...}}` placeholders.** Just write `Project:` and let people fill it in.
4. **English**, technical terms may stay as they are.
5. **No marketing language.** No "innovative solution", "seamless", "cutting-edge", "in the digital era".
6. **Keep the document count small.** Nine is already the upper bound. Adding a document means every
   user fills in one more file before starting work — that is a real cost, not completeness.

---

## File naming

`AGENT-RULES.md` is deliberately **not** named `AGENTS.md` in this repo. A file with that name would
be read by most AI agents as the contract for *this repo*, which makes the kit look like an
application project — exactly the confusion this repo exists to avoid. `new_project.py` renames it to
`AGENTS.md` when copying.

All file names under `docs/` and the repo root **must be lowercase** with hyphen separators
(`00-problem.md`, not `00_Problem.md`). `README.md` and `AGENTS.md` are the only exceptions, because
those names are conventions that agents and platforms already recognize.

---

## Changing a document

1. Fork, create a branch: `git checkout -b fix/short-description`
2. Make the change.
3. Verify the copy still works:

```bash
python -m py_compile scripts/new_project.py
python scripts/new_project.py --dry-run --target ./out/dryrun
python scripts/new_project.py --target ./out/project-a
python scripts/new_project.py --target ./out/project-b --force
ls ./out/project-b/docs
```

4. Update `docs/README.md` and `README.md` if a file name or the file count changed.
5. Open a pull request: state **which mistake your change prevents**.

---

## What we do not accept

- Adding examples, filled-in examples, or a sample project
- Adding a new document without removing another (unless the reason is very strong)
- Adding columns without explaining the benefit
- Removing the "out of scope", "parking lot", or "open questions" sections — those three prevent
  projects from drifting more than anything else
- Default technology recommendations (microservices, AI, blockchain) with no link to a requirement

---

## Reporting a problem

```
Document : [file name]
Section  : [section heading]
Problem  : [e.g. the question is ambiguous / the column is never used / the answer is unclear]
Proposal : [if you have one]
```

If two documents contradict each other (`01-requirements.md` against `02-design.md`), that is a
serious finding — report it.
