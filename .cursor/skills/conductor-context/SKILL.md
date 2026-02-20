---
name: conductor-context
description: Provides context about Conductor project management files. Use when the user mentions plans, tracks, specs, conductor, or when working with conductor/ directory files.
---

# Conductor Context

If a user mentions a "plan" or asks about the plan, and they have used the Conductor framework in the current session, they are likely referring to the `conductor/tracks.md` file or one of the track plans (`conductor/tracks/<track_id>/plan.md`).

## Universal File Resolution Protocol

**PROTOCOL: How to locate files.**
To find a file (e.g., "**Product Definition**") within a specific context (Project Root or a specific Track):

1.  **Identify Index:** Determine the relevant index file:
    -   **Project Context:** `conductor/index.md`
    -   **Track Context:**
        a. Resolve and read the **Tracks Registry** (via Project Context).
        b. Find the entry for the specific `<track_id>`.
        c. Follow the link provided in the registry to locate the track's folder. The index file is `<track_folder>/index.md`.
        d. **Fallback:** If the track is not yet registered (e.g., during creation) or the link is broken:
            1. Resolve the **Tracks Directory** (via Project Context).
            2. The index file is `<Tracks Directory>/<track_id>/index.md`.

2.  **Check Index:** Read the index file and look for a link with a matching or semantically similar label.

3.  **Resolve Path:** If a link is found, resolve its path **relative to the directory containing the `index.md` file**.
    -   *Example:* If `conductor/index.md` links to `./workflow.md`, the full path is `conductor/workflow.md`.

4.  **Fallback:** If the index file is missing or the link is absent, use the **Default Path** keys below.

5.  **Verify:** You MUST verify the resolved file actually exists on the disk.

**Standard Default Paths (Project):**
- **Product Definition**: `conductor/product.md`
- **Tech Stack**: `conductor/tech-stack.md`
- **Workflow**: `conductor/workflow.md`
- **Product Guidelines**: `conductor/product-guidelines.md`
- **Tracks Registry**: `conductor/tracks.md`
- **Tracks Directory**: `conductor/tracks/`

**Standard Default Paths (Track):**
- **Specification**: `conductor/tracks/<track_id>/spec.md`
- **Implementation Plan**: `conductor/tracks/<track_id>/plan.md`
- **Metadata**: `conductor/tracks/<track_id>/metadata.json`

---

## Tool Call Validation Protocol

Every Conductor skill includes the rule: *"You must validate the success of every tool call."* This section defines **how** to validate.

### Shell Commands (git, npm, etc.)
1.  **ONE COMMAND PER CALL:** You MUST run each meaningful shell command as a **separate** Shell tool call. Do NOT chain commands with `&&` or `;`. The only exception is pipes (`|`) for filtering output.
    -   **Correct:** Call 1: `git add file.txt` → validate → Call 2: `git commit -m "msg"` → validate
    -   **Wrong:** `git add file.txt && git commit -m "msg"` (if `git add` silently skips files, the commit still runs)
2.  **Check the output.** After every shell command, read the tool result. Look for error indicators: `error:`, `fatal:`, `CONFLICT`, `failed`, `not found`, `permission denied`, non-zero exit codes.
3.  **Git-specific validations:**
    -   **`git add`**: After staging, run `git status --porcelain` and confirm the intended files appear as staged (`A`, `M`, `R` in the first column). If files are missing from the staging area, re-add them.
    -   **`git commit`**: The output MUST contain a line like `[branch hash] commit message`. If the output contains `nothing to commit`, `error`, or `aborting`, the commit **failed** — do NOT proceed as if it succeeded.
    -   **`git revert`**: The output MUST confirm the revert commit was created. If it shows `CONFLICT` or `error`, halt and inform the user.
    -   **`git diff` / `git log`**: If the output is empty when you expected content, re-check your arguments (commit range, file paths) before proceeding.
4.  **On failure:** Do NOT silently continue. You MUST:
    a. Stop the current operation.
    b. Report the exact error output to the user.
    c. Suggest a remediation if obvious.
    d. Await user instructions before retrying.

### File Operations (Read, Write, StrReplace)
1.  **Read:** If a file read returns an error (file not found, permission denied), do NOT assume the file is empty or proceed with placeholder content. Halt and report.
2.  **Write / StrReplace:** After writing or editing a file, if the tool reports an error, halt and report. Do NOT assume the write succeeded.

### General Rule
If you are **uncertain** whether a tool call succeeded (e.g., ambiguous output, unexpected format), treat it as a **failure** and ask the user to verify. Never assume success when in doubt.

---

## Slash Command Boundaries

**CRITICAL — KNOW WHEN NOT TO USE CONDUCTOR:** Not every code change requires the Conductor workflow. If the user asks for a small, isolated change (e.g., adjust a layout, change a color, rename a label, fix a typo, tweak CSS), you should **directly edit the code** without creating a new track or invoking `/conductor-implement`. Conductor tracks are for **planned, multi-task features or bug fixes** — not for ad-hoc tweaks. Use your judgment:
- **Use Conductor:** "Add user authentication", "Build a settings page", "Refactor the database layer"
- **Do NOT use Conductor:** "Move this button to the left", "Change the font size", "Add waist circumference back to the dashboard"
