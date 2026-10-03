# 02 — Design

> Fill this in after the requirements are clear. Design follows the requirements, not the other way round.

**Project:**
**Stack:**
**Date:**

---

## 1. System boundary

**Inside the system:**

- 

**Outside the system** (handled by people / other systems):

- 

---

## 2. Components

| Component | Responsibility (just one) | Technology | Why so |
|---|---|---|---|
| | | | |
| | | | |

---

## 3. Data flows

| From | To | Data | How | If it fails |
|---|---|---|---|---|
| | | | | |
| | | | | |

---

## 4. Interfaces

Commands (CLI), endpoints (API), or screens (application) — depending on the shape of the project.

| Interface | What for | Input | Output | Requirement |
|---|---|---|---|---|
| | | | | |
| | | | | |

---

## 5. Access control

| Role | May view | May create | May edit | May delete |
|---|---|---|---|---|
| | | | | |
| | | | | |

**Enforced on the server?** 

If not enforced, state its limits and what actually protects it (e.g. a physical barrier).

---

## 6. Configuration & secrets

| Variable | Purpose | Required | Example value |
|---|---|---|---|
| | | | |
| | | | |

Rule: secrets are never written in code or documents. `.env` does not go into git.

---

## 7. Run & deploy

**Locally:**

```
```

**Deploy:**

```
```

**Rollback:**

**Backup:**

---

## 8. Deliberately rejected technology

| Technology | Why not used | When it might be needed |
|---|---|---|
| | | |
