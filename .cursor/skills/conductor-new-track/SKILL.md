---
name: conductor-new-track
description: Creates a new track (feature, bug fix, or chore) with interactive spec and plan generation. Use when the user wants to plan a new feature or work item.
disable-model-invocation: true
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent assistant for the Conductor spec-driven development framework. Your current task is to guide the user through the creation of a new "Track" (a feature or bug fix), generate the necessary specification (`spec.md`) and plan (`plan.md`) files, and organize them within a dedicated track directory.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Conductor environment is properly set up.**

1.  **Verify Core Context:** Using the **Universal File Resolution Protocol** (defined in the `conductor-context` skill), resolve and verify the existence of:
    -   **Product Definition**
    -   **Tech Stack**
    -   **Workflow**

2.  **Handle Failure:**
    -   If ANY of these files are missing, you MUST halt the operation immediately.
    -   Announce: "Conductor is not set up. Please run `/conductor-setup` to set up the environment."
    -   Do NOT proceed to New Track Initialization.

---

## 2.0 NEW TRACK INITIALIZATION
**PROTOCOL: Follow this sequence precisely.**

### 2.1 Get Track Description and Determine Type

1.  **Load Project Context:** Read and understand the content of the project documents (**Product Definition**, **Tech Stack**, etc.) resolved via the **Universal File Resolution Protocol**.
2.  **Get Track Description:**
    *   If the user provided a description alongside the `/conductor-new-track` invocation, use it.
    *   Otherwise, ask: "Please provide a brief description of the track (feature, bug fix, chore, etc.) you wish to start."
3.  **Infer Track Type:** Analyze the description to determine if it is a "Feature" or "Something Else" (e.g., Bug, Chore, Refactor). Do NOT ask the user to classify it.

### 2.2 Interactive Specification Generation (`spec.md`)

1.  **State Your Goal:** Announce:
    > "I'll now guide you through a series of questions to build a comprehensive specification (`spec.md`) for this track."

2.  **Questioning Phase:** Ask questions to gather details for `spec.md`. Tailor based on track type.
    *   **CRITICAL:** Ask questions sequentially (one by one). Wait for user response before next question.
    *   **General Guidelines:**
        *   Refer to **Product Definition**, **Tech Stack** for context-aware questions.
        *   Present 2-3 plausible options (A, B, C) when possible.
        *   Last option: "Type your own answer".
        *   Classify questions as "Additive" or "Exclusive Choice".
    *   **If FEATURE:** Ask 3-5 relevant questions.
    *   **If SOMETHING ELSE (Bug, Chore, etc.):** Ask 2-3 relevant questions.

3.  **Draft `spec.md`:** Generate content including Overview, Functional Requirements, Non-Functional Requirements, Acceptance Criteria, and Out of Scope.

4.  **User Confirmation:** Present and iterate until approved.

### 2.3 Interactive Plan Generation (`plan.md`)

1.  **State Your Goal:** Once `spec.md` is approved, announce plan generation.

2.  **Generate Plan:**
    *   Read confirmed `spec.md` content.
    *   Resolve and read the **Workflow** file.
    *   Generate `plan.md` with Phases, Tasks, and Sub-tasks.
    *   **CRITICAL:** Plan structure MUST adhere to **Workflow** methodology (e.g., TDD).
    *   Include `[ ]` status markers for every task and sub-task:
        - Parent: `- [ ] Task: ...`
        - Sub-task: `    - [ ] ...`
    *   **Inject Phase Completion Tasks** if defined in Workflow.

3.  **User Confirmation:** Present and iterate until approved.

### 2.4 Create Track Artifacts and Update Main Plan

1.  **Check for existing track name:** List existing track directories. If proposed short name matches, halt and suggest different name.
2.  **Generate Track ID:** `shortname_YYYYMMDD` format.
3.  **Create Directory:** `<Tracks Directory>/<track_id>/`.
4.  **Create `metadata.json`:**
    ```json
    {
      "track_id": "<track_id>",
      "type": "feature",
      "status": "new",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
      "description": "<Initial user description>"
    }
    ```
5.  **Write Files:** `spec.md`, `plan.md`, and `index.md` in the track directory.
6.  **Update Tracks Registry:** Append new track section:
    ```markdown

    ---

    - [ ] **Track: <Track Description>**
    *Link: [./<Relative Track Path>/](./<Relative Track Path>/)*
    ```
7.  **Commit All Track Artifacts:** Stage and commit with `chore(conductor): Add new track '<track_description>'`.
8.  **Announce Completion:** Inform user to run `/conductor-implement`.
