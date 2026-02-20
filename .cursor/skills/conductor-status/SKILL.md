---
name: conductor-status
description: Displays the current progress of all tracks in the project. Use when the user wants to see project status, track progress, or task completion overview.
disable-model-invocation: true
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to provide a status overview of the current tracks file. This involves reading the **Tracks Registry** file, parsing its content, and summarizing the progress of tasks.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Conductor environment is properly set up.**

1.  **Verify Core Context:** Using the **Universal File Resolution Protocol** (defined in the `conductor-context` skill), resolve and verify the existence of:
    -   **Tracks Registry**
    -   **Product Definition**
    -   **Tech Stack**
    -   **Workflow**

2.  **Handle Failure:**
    -   If ANY of these files are missing, you MUST halt the operation immediately.
    -   Announce: "Conductor is not set up. Please run `/conductor-setup` to set up the environment."
    -   Do NOT proceed to Status Overview Protocol.

---

## 2.0 STATUS OVERVIEW PROTOCOL
**PROTOCOL: Follow this sequence to provide a status overview.**

### 2.1 Read Project Plan
1.  **Locate and Read:** Read the content of the **Tracks Registry** (resolved via **Universal File Resolution Protocol**).
2.  **Locate and Read Tracks:**
    -   Parse the **Tracks Registry** to identify all registered tracks and their paths.
        *   **Parsing Logic:** Look for lines matching either `- [ ] **Track:` or `## [ ] Track:`.
    -   For each track, resolve and read its **Implementation Plan** (using **Universal File Resolution Protocol** via the track's index file).

### 2.2 Parse and Summarize Plan
1.  **Parse Content:**
    -   Identify major project phases/sections (e.g., top-level markdown headings).
    -   Identify individual tasks and their current status.
2.  **Generate Summary:** Create a concise summary including:
    -   Total number of major phases.
    -   Total number of tasks.
    -   Number of tasks completed, in progress, and pending.

### 2.3 Present Status Overview
1.  **Output Summary:** Present the generated summary in a clear, readable format:
    -   **Current Date/Time:** The current timestamp.
    -   **Project Status:** High-level summary (e.g., "On Track", "Behind Schedule", "Blocked").
    -   **Current Phase and Task:** The specific phase and task currently marked as "IN PROGRESS".
    -   **Next Action Needed:** The next task listed as "PENDING".
    -   **Blockers:** Any items explicitly marked as blockers.
    -   **Phases (total):** Total number of major phases.
    -   **Tasks (total):** Total number of tasks.
    -   **Progress:** `tasks_completed/tasks_total (percentage%)`.
