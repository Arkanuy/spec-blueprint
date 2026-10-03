# Project documents

Nine documents, filled in order when starting a new project. All of them are still empty —
the content comes from you, not from this repo.

If the documents and the code disagree, the documents win — or the documents are updated first,
then the code.

---

## Filling order

Do not skip ahead. Each document answers one question, and the next document depends
on the previous answer.

| # | Document | Answers | Done when |
|---|---|---|---|
| 0 | [00-problem.md](00-problem.md) | What problem is being solved, and is a system really the answer? | There is one main problem + root cause + reasoned solution choices |
| 1 | [01-requirements.md](01-requirements.md) | What behaviour must be met | Every P0 feature has an ID'd requirement + acceptance criteria |
| 2 | [02-design.md](02-design.md) | How the system is put together | There is a system boundary, components, and access control |
| 3 | [03-process.md](03-process.md) | How the work runs now vs after | There is a NOW process, an AFTER process, and a mapping of the problems |
| 4 | [04-data.md](04-data.md) | What data is stored | There are entities, fields, rules, and a lifecycle |
| 5 | [05-ui.md](05-ui.md) | What the user sees | Every screen has empty, loading, and failure states |
| 6 | [06-testing.md](06-testing.md) | How it is proven correct | Every P0 requirement has at least one test case |
| 7 | [07-build-order.md](07-build-order.md) | How it is worked through in order | There are phases, a feature order, and a definition of done |
| 8 | [08-risks.md](08-risks.md) | What can fail, and why decisions are made | There are risks, assumptions, open questions, and a decision log |

---

## ID format

All IDs are written as **prefix + three digits**: `PREFIX-001`, `PREFIX-002`, and so on.

| Prefix | Meaning | Used in |
|---|---|---|
| `US` | User story | `01-requirements.md` |
| `FR` | Functional requirements | `01-requirements.md` |
| `NFR` | Non-functional requirements | `01-requirements.md` |
| `BR` | Business rules | `01-requirements.md` |
| `DR` | Data requirements | `01-requirements.md` |
| `TC` | Test cases | `06-testing.md` |

---

## Filling rules

1. **One document, one audience.** `00` and `01` are read by the product owner; `02` and `04` by the
   developer; `06` by the tester.
2. **Mark the origin of a claim.** Write `(Fact)`, `(Assumption)`, or `(Needs confirmation)` after a
   claim whose origin is unclear.
3. **Every feature can be traced** back to a problem in `00-problem.md`.
4. **Do not invent numbers that have no data yet.** Write `[needs data]`, then record it in
   `08-risks.md`.

---

## Context for AI agents

```
docs/01-requirements.md  +  docs/02-design.md  +  docs/04-data.md  +  docs/05-ui.md  +  AGENTS.md
```

The one hard rule: **AI must not write a feature that has no requirement ID.** Extra ideas
go into `00-problem.md` under "Parking lot" first, not straight into code.
