# Writing Standards & README Sync — RFX1427 Finance

> Authority: This document is authoritative. All commits on `mistral-fix5th` / `master` MUST comply.

## 1. Language Rule — ENGLISH ONLY for Committed Writing

- **Conversation language** (chat with user) MAY be Bahasa Melayu / Indonesia / English — no restriction.
- **Committed writing** (anything that goes into git) MUST be **English only**:
  - `README.md`, `SKILL.md`, `pyproject.toml`, `references/*.md`, `agents/*.yaml`, code docstrings/comments visible to users, commit messages, PR descriptions, Change Log.
- Exceptions (allowed non-English):
  - `WAJIB 7` — branded label for "Mandatory 7" (keep as-is, do not translate).
  - Fail-safe disclaimer string: `"Hanya X peluang memenuhi gate daripada semua sumber — tidak dapat capai 7 tanpa melanggar hard gate."` — locked Bahasa string (do not translate).
  - User-selected `output_language` report output — follows Gate 0 choice, not this rule.
- Enforcement: Before every commit, grep for stray Malay/Indonesia in the 8 files above. If found, translate to English before commit.

## 2. README Sync Rule — Single Source of Truth

- `SKILL.md` is the **source of truth** for framework version, Hard Rules, and Phase logic.
- `README.md` MUST mirror `SKILL.md` in the **same commit** — never in a follow-up commit.
- Files that participate in sync (must be checked together):

| Source of truth | Must sync to README |
|-----------------|---------------------|
| `SKILL.md` Version header (e.g. 4.7) | Badge `version-4.7-blue` + Overview + Change Log |
| `SKILL.md` Hard Rule #7 / #36 | README Hard Rules #7 |
| `SKILL.md` Python Rules / Fallback Architecture / Step 1F | README Phase 1 Scanner (2 paragraphs) |
| `SKILL.md` Phase 1 Output template | README Workflow diagram + locked report line |
| `pyproject.toml` version | README badge + Change Log |
| `references/phase1-scanner.md` `references/hard-rules-master.md` `references/error-states.md` | README sections that reference them |

## 3. Change Workflow (Mandatory Checklist)

Before `git commit` on `mistral-fix5th`:

- [ ] 1. All changed docs written in English (except allowed exceptions)
- [ ] 2. `README.md` updated in same commit if any of SKILL/refs/pyproject changed
- [ ] 3. `grep -n "4\." README.md SKILL.md pyproject.toml` — version consistent
- [ ] 4. `grep -n "WAJIB\|Exactly 7\|7–10\|50→70→100" README.md SKILL.md references/phase1-scanner.md` — logic consistent
- [ ] 5. `python -m pytest -q` — 14 passed
- [ ] 6. `git status --porcelain` — clean after commit

## 4. Diagram Rule

- `README.md > End-to-End Workflow` diagram line for Phase 1 MUST use staged wording:
  `Python source fetch → AI reads staged pool 50→70→100 (early-stop) → Best 7–10 positive opportunities (WAJIB 7 target 10)`
  Never `Best 7` alone.

## 5. Violation

Any commit that changes SKILL/refs/pyproject without README sync is considered **incomplete** and must be amended before PR/merge.
