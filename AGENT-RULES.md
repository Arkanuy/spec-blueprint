# Working rules for AI agents in this project

> This file is a contract between the project owner and AI agents (Claude Code, Codex, Cursor,
> Copilot, Hermes, or any other). The agent must read `docs/` before writing code.
> Copied into your project as `AGENTS.md`.

**Project:**
**Stack:**
**Product owner:**

---

## 1. Read first

| Order | File | Why |
|---|---|---|
| 1 | `docs/00-problem.md` | Know which problem is being solved and where the boundary is |
| 2 | `docs/01-requirements.md` | Know the required behavior (FR/NFR/BR) |
| 3 | `docs/02-design.md` | Know the component layout and technical boundary |
| 4 | `docs/04-data.md` | Know the correct data structure |
| 5 | `docs/05-ui.md` | Know the screens and every failure state |
| 6 | `docs/08-risks.md` | Know the unverified assumptions |

If a section is still empty, **do not guess**. Ask, or mark that work as blocked.

---

## 2. Rules that must not be broken

1. **No feature without a requirement ID.** Every task references an `FR-xxx` in `docs/01-requirements.md`. If it does not exist yet, ask for it first.
2. **Do not change scope.** New feature ideas go to the "Parking lot" section of `docs/00-problem.md` first, not straight into code.
3. **Do not guess business rules.** If a rule is unclear, ask. Do not pick one yourself.
4. **Do not add new dependencies** without approval; record the reason.
5. **Never write secrets in code.** Credentials come from environment variables only; `.env` never goes into git.
6. **Validation is enforced on the server.** Hiding a button in the UI is not security.
7. **Do not change approved behavior** without recording it in `docs/08-risks.md`.
8. **Always handle failure states**: empty, loading, and error.

---

## 3. Workflow per task

```
1. READ       → read the documents relevant to this task
2. CONFIRM    → restate the task in one sentence + name the requirement it serves
3. PLAN       → list the files you will touch and your approach
4. BUILD      → implement only within that scope
5. TEST       → run the related test cases (docs/06-testing.md)
6. REPORT     → what changed, the evidence, what is unfinished
7. RECORD     → update the docs if reality shifted
```

One task, one scope. Do not work on two features in a single change.

---

## 4. Report format

```
Task        : [what was done]
Requirement : [requirement ID this serves]
Files       : [files changed]
Test        : [test case ID] pass / fail — [evidence: command output]
Not done    : [deliberately left out]
Risk        : [what to watch out for]
Docs        : [documents updated]
```

If there is no real test evidence, write **"not tested"** — never write "should work".

---

## 5. Code standards

| Aspect | Rule |
|---|---|
| Style | Follow the conventions already in the repo |
| Function size | One function, one responsibility |
| Comments | Explain **why**, not what |
| Error handling | Never swallow errors silently; handle or propagate with context |
| Validation | At the system boundary (input) and at the data layer |
| Logging | Log important events; never log sensitive data |
| UI language | |
| Comment language | |

---

## 6. Prohibitions

An agent must **not**:

- Recreate a file that already exists without reading it first
- Delete or overwrite someone else's work without cause
- Run destructive commands (`rm -rf`, database reset, force push) without explicit permission
- Change the database schema without a migration
- Disable a failing test so it looks green
- Add placeholders that make code look complete but do nothing
- Claim something is finished without running it

---

## 7. When information is missing

```
Blocked  : [work that stopped]
Need     : [the specific information]
Why      : [how it changes the decision]
Meanwhile: [assumption used if work must continue — flagged clearly]
```

Only ask what actually blocks you.

---

## 8. Language

- Default language for communication: **English**
- Keep technical terms as they are, with a short explanation the first time
- Avoid marketing language ("innovative", "seamless", "cutting-edge", "in the digital era")

---

## 9. Known traps

Fill this table with real lessons from the project. If you find a new trap, write it here.

| Trap | How to avoid it |
|---|---|
| | |
