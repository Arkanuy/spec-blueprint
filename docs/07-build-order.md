# 07 — Build Order

> One task, one scope. Do not work on two features at the same time.

**Project:**
**Date:**

---

## 1. Ordering principles

| # | Principle | Reason |
|---|---|---|
| 1 | Data schema first | Every layer above it depends on this |
| 2 | Business rules before the UI | Correct rules do not depend on the UI |
| 3 | Failure paths before extra features | A product that does not handle failure is not usable yet |
| 4 | | |

---

## 2. Phases

| Phase | Content | Output | Done when |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

---

## 3. Per-feature order

| Order | Feature | Requirement | Phase |
|---|---|---|---|
| 1.1 | | | 1 |
| 1.2 | | | 1 |

---

## 4. Definition of done (per feature)

- [ ] Behaviour matches the requirement and its acceptance criteria
- [ ] Business rules are enforced on the server, not only in the UI
- [ ] Empty, loading, and failure states are handled
- [ ] An access check exists on the server
- [ ] Input validation exists with messages the user can understand
- [ ] The related test cases are run and pass, with evidence
- [ ] There are no new errors in the log
- [ ] The documents are updated if anything shifted

---

## 5. Milestones

| Milestone | Content | How to check | Date |
|---|---|---|---|
| | | | |
| | | | |
