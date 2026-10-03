# Spec Blueprint

Empty documents for you to fill in when you start a new project. Nine `.md` files in `docs/`,
one contract for AI agents, and one script to copy them.

Not an application. Not a sample project. The documents are empty on purpose — they are yours to fill.

---

## Why

Ask an AI to write code with no documents and it will guess. AI guesses always look reasonable —
until the scope explodes, the screens do not match how the work actually runs, and nobody knows
which features are genuinely needed.

| Symptom | Root cause |
|---|---|
| More features appear, the product gets less clear | The problem and the goal were never written down |
| The AI builds things nobody asked for, or misses the important ones | No traceable requirements |
| Code is inconsistent between sessions | No design boundary or conventions |
| Scope creeps without anyone noticing | No explicit in-scope / out-of-scope list |
| Hard to judge what the AI produced | No definition of done |
| Decisions lose their history | No decision log |

---

## Contents

```
docs/
├── README.md              # fill-in order + ID format
├── 00-problem.md          # problem, root cause, impact, solution alternatives, scope
├── 01-requirements.md     # users, user stories, FR/NFR/BR/DR, acceptance criteria, traceability
├── 02-design.md           # system boundary, components, data flows, access control, deploy
├── 03-process.md          # process NOW vs AFTER, statuses, failure conditions
├── 04-data.md             # entities, fields, relationships, rules, lifecycle, sensitive data
├── 05-ui.md               # screens, elements, every state (empty/loading/failure/success)
├── 06-testing.md          # strategy, test cases, non-happy-path cases, evidence
├── 07-build-order.md      # phases, per-feature order, definition of done, milestones
└── 08-risks.md            # scored risks, assumptions, open questions, decision log
AGENT-RULES.md             # the agent contract — copied into your project as AGENTS.md
scripts/new_project.py     # copies docs/ + AGENTS.md into a new project folder
```

Nine documents, not twelve. Only the ones that get used — nothing kept just to look complete.
Roughly 900 lines for all nine, so none of them is heavy to fill in.

---

## Usage

```bash
git clone https://github.com/Arkanuy/spec-blueprint.git
cd spec-blueprint
python scripts/new_project.py --target ~/projects/my-project
```

No script? Copy it by hand — the source file is `AGENT-RULES.md`, but name it `AGENTS.md` in your
folder so AI agents pick it up automatically:

```bash
mkdir -p ~/projects/my-project
cp -r docs ~/projects/my-project/
cp AGENT-RULES.md ~/projects/my-project/AGENTS.md
```

Then fill them in in order, starting with `docs/00-problem.md`. The full order is in `docs/README.md`.

Flags for `new_project.py`:

| Flag | Meaning |
|---|---|
| `--target` | New project folder (required) |
| `--force` | Allow writing into a folder that already contains files |
| `--dry-run` | Show the plan without writing anything |

---

## Fill-in order

```
1. PROBLEM      → 00-problem.md       what is wrong, why, is a system even the answer?
2. REQUIREMENTS → 01-requirements.md  what behavior must hold (with IDs, testable)
3. DESIGN       → 02-design.md        how it is built, where the boundary is
4. PROCESS      → 03-process.md       now vs after
5. DATA         → 04-data.md          what is stored and what keeps it correct
6. UI           → 05-ui.md            what the user sees, including failure states
7. TESTING      → 06-testing.md       how it is proven correct
8. BUILD ORDER  → 07-build-order.md   what order work ships in
9. RISKS        → 08-risks.md         what can fail, why decisions were made
```

The one hard rule: **do not ask an AI to write a feature that has no requirement ID.**

---

## Principles

1. **Problem first, technology last.** Technology is chosen because of a need, not the other way around.
2. **Every feature traces** to problem → requirement → code → test.
3. **Separate facts, assumptions, and guesses.** Anything unverified is written down as such.
4. **A small but clear scope beats** a large vague one.
5. **No requirement that cannot be tested.**
6. **No decorative columns.** Every section must prevent one real kind of mistake.

---

## For Information Systems coursework

This structure maps onto the artifacts usually required in Systems Analysis & Design courses:
business context, stakeholders, as-is/to-be, functional and non-functional requirements, business
rules, data model, use cases, and a feasibility justification.

The part students most often leave out — *why the problem is real* and *why the solution is
proportional* — is handled in `00-problem.md` (the root-cause section and the solution-alternatives
table, which includes the no-system option) and `07-build-order.md`.

---

## License

MIT.
