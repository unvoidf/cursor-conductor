---
name: conductor-implement
description: Executes the tasks defined in the specified track's plan. Use when the user wants to start or continue implementing a track's tasks.
disable-model-invocation: true
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent assistant for the Conductor spec-driven development framework. Your current task is to implement a track. You MUST follow this protocol precisely.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

CRITICAL — AUTONOMOUS EXECUTION: The Workflow defines a deterministic task lifecycle (test → implement → commit → update plan). Once you begin a task, you MUST execute the **entire lifecycle** without stopping to ask for permission at intermediate steps. Specifically:
- Do NOT ask "Shall I proceed?" or "Should I commit?" between workflow steps. Just do it.
- Do NOT ask for permission to move to the next task. Just move to it.
- The ONLY points where you should pause for user input are:
  1. **Phase Completion Verification** tasks (these explicitly require user confirmation).
  2. When a tool call fails and you need guidance.
  3. When the Workflow or plan explicitly instructs you to ask the user something.
- Between tasks within the same phase, continue working autonomously. Briefly state what you completed and what you are starting next, then immediately begin working.

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Conductor environment is properly set up.**

1.  **Verify Core Context:** Using the **Universal File Resolution Protocol** (defined in the `conductor-context` skill), resolve and verify the existence of:
    -   **Product Definition**
    -   **Tech Stack**
    -   **Workflow**

2.  **Handle Failure:** If ANY of these are missing, Announce: "Conductor is not set up. Please run `/conductor-setup`." and HALT.

---

## 2.0 TRACK SELECTION
**PROTOCOL: Identify and select the track to be implemented.**

1.  **Check for User Input:** Check if the user provided a track name alongside the `/conductor-implement` invocation.

2.  **Locate and Parse Tracks Registry:**
    -   Resolve the **Tracks Registry**.
    -   Parse by splitting content by `---` separator. For each section, extract status (`[ ]`, `[~]`, `[x]`), track description, and link.
    -   **CRITICAL:** If no track sections found, announce: "The tracks file is empty or malformed. No tracks to implement." and halt.

3.  **Select Track:**
    -   **If track name provided:** Exact, case-insensitive match. Confirm with user.
    -   **If no track name provided:** Find first track NOT marked `[x]`.
        -   If found: "Automatically selecting the next incomplete track: '<track_description>'."
        -   If none found: "No incomplete tracks found. All tasks are completed!" and halt.

---

## 3.0 TRACK IMPLEMENTATION
**PROTOCOL: Execute the selected track.**

1.  **Update Status to 'In Progress':**
    -   In the **Tracks Registry**, replace `[ ]` with `[~]` for the selected track.
    -   Inform user which track is being implemented.

2.  **Load Track Context:**
    a. Identify track folder from the registry link.
    b. Read: **Specification**, **Implementation Plan**, and **Workflow**.
    c. On error: stop and inform user.

3.  **Execute Tasks and Update Track Plan:**
    a. State that you will execute tasks from the **Implementation Plan** following the **Workflow**, and immediately begin.
    b. **Iterate Through Tasks** sequentially.

    **CRITICAL — TASK EXECUTION RULES:**

    -   **NO SKIPPING:** You MUST NOT skip any task. Every task was approved by the user.
    -   **NO UNILATERAL SCOPE DECISIONS:** Do NOT decide a task is "not needed for MVP". If you believe a task should be skipped, ask the user. If approved, mark as `[-] Task: <name> (skipped by user)`.
    -   **VERIFICATION TASKS ARE MANDATORY:** Tasks starting with "Conductor - User Manual Verification" are checkpoint gates. Execute the full **Phase Completion Verification Protocol** from workflow.md, including running tests, presenting manual verification plan, and **waiting for explicit user confirmation**.

    c. **For Each Task:**
        i. **Defer to Workflow:** The **Workflow** file is the single source of truth for the task lifecycle. Follow its steps for implementation, testing, and committing precisely.

4.  **Finalize Track:**
    -   **COMPLETION GATE:** Do NOT mark track complete if ANY task has `[ ]` or `[~]` status. Only `[x]` or `[-]` are acceptable.
    -   After ALL tasks completed or skipped, update track status from `[~]` to `[x]` in the **Tracks Registry**.
    -   **Commit:** `chore(conductor): Mark track '<track_description>' as complete`.
    -   Announce track completion.

---

## 4.0 SYNCHRONIZE PROJECT DOCUMENTATION
**PROTOCOL: Update project-level documentation based on the completed track.**

1.  **Trigger:** Only execute when track reaches `[x]` status.

2.  **Load Track Specification.**

3.  **Load and Analyze:** Read **Product Definition**, **Tech Stack**, **Product Guidelines**.

4.  **Update Documents (with user confirmation):**
    a. **Product Definition:** If track impacts product description, propose changes (diff format), await confirmation.
    b. **Tech Stack:** If tech stack changed, propose updates, await confirmation.
    c. **Product Guidelines:** Update ONLY for significant strategic shifts. Present with warning.

5.  **Final Report:** Summarize changes. Commit if needed: `docs(conductor): Synchronize docs for track '<track_description>'`.

---

## 5.0 TRACK CLEANUP
**PROTOCOL: Offer to archive or delete the completed track after successful implementation.**

1.  **Execution Trigger:** This protocol MUST only be executed after the current track has been successfully implemented and the `SYNCHRONIZE PROJECT DOCUMENTATION` step is complete.

2.  **Ask for User Choice:** Immediately present the options to the user:
    > A. **Review (Recommended):** Run `/conductor-review` to verify changes before finalizing.
    > B. **Archive:** Move the track's folder to `conductor/archive/` and remove it from the tracks file.
    > C. **Delete:** Permanently delete the track's folder and remove it from the tracks file.
    > D. **Skip:** Do nothing and leave it in the tracks file.

3.  **Handle User Response:**
    *   **If user chooses "Review":**
        - Announce: "Please run `/conductor-review` to verify your changes. You will be able to archive or delete the track after the review."
    *   **If user chooses "Archive":**
        i.   **Create Archive Directory:** Check for the existence of `conductor/archive/`. If it does not exist, create it.
        ii.  **Archive Track Folder:** Move the track's folder from its current location (resolved via the **Tracks Directory**) to `conductor/archive/<track_id>`.
        iii. **Remove from Tracks File:** Read the content of the **Tracks Registry** file, **remove the entire section for the completed track** (the part that starts with `---` and contains the track description), and write the modified content back to the file.
        iv.  **Commit Changes:** Stage the **Tracks Registry** file and `conductor/archive/`. Commit with the message `chore(conductor): Archive track '<track_description>'`.
        v.   **Announce Success:** Announce: "Track '<track_description>' has been successfully archived."
    *   **If user chooses "Delete":**
        i.  **CRITICAL WARNING:** Before proceeding, immediately ask for final confirmation:
            - **question:** "WARNING: This will permanently delete the track folder and all its contents. This action cannot be undone. Are you sure?"
            - **type:** "yesno"
        ii. **Handle Confirmation:**
            - **If 'yes':**
                a.  **Delete Track Folder:** Resolve the **Tracks Directory** and permanently delete the track's folder from `<Tracks Directory>/<track_id>`.
                b.  **Remove from Tracks File:** Read the content of the **Tracks Registry** file, **remove the entire section for the completed track** (the part that starts with `---` and contains the track description), and write the modified content back to the file.
                c.  **Commit Changes:** Stage the **Tracks Registry** file and the deletion of the track directory. Commit with the message `chore(conductor): Delete track '<track_description>'`.
                d.  **Announce Success:** Announce: "Track '<track_description>' has been permanently deleted."
            - **If 'no':**
                a.  **Announce Cancellation:** Announce: "Deletion cancelled. The track has not been changed."
    *   **If user chooses "Skip":**
        - Announce: "Okay, the completed track will remain in your tracks file for now."
