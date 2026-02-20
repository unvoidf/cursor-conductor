---
name: conductor-setup
description: Scaffolds the project and sets up the Conductor environment. Use when the user wants to initialize Conductor for a new or existing project.
disable-model-invocation: true
---

## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to set up and manage a software project using the Conductor methodology. This document is your operational protocol. Adhere to these instructions precisely and sequentially. Do not make assumptions.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

**TEMPLATE RESOLUTION:** When this protocol requires copying template files (such as workflow.md or code styleguides), you must locate them in the Conductor skill's `assets/` directory. The templates are bundled with this skill at:
- Workflow template: `assets/workflow.md` (relative to this SKILL.md)
- Code styleguides: `assets/code_styleguides/` (relative to this SKILL.md)

To find the absolute path, look for `.cursor/skills/conductor-setup/assets/` in the project root, or `~/.cursor/skills/conductor-setup/assets/` for user-level installation. If templates cannot be found, generate the content inline based on best practices.

---

## 1.1 PRE-INITIALIZATION OVERVIEW
1.  **Provide High-Level Overview:**
    -   Present the following overview of the initialization process to the user:
        > "Welcome to Conductor. I will guide you through the following steps to set up your project:
        > 1. **Project Discovery:** Analyze the current directory to determine if this is a new or existing project.
        > 2. **Product Definition:** Collaboratively define the product's vision, design guidelines, and technology stack.
        > 3. **Configuration:** Select appropriate code style guides and customize your development workflow.
        > 4. **Track Generation:** Define the initial **track** (a high-level unit of work like a feature or bug fix) and automatically generate a detailed plan to start development.
        >
        > Let's get started!"

---

## 1.2 BEGIN `RESUME` CHECK
**PROTOCOL: Before starting the setup, determine the project's state using the state file.**

1.  **Read State File:** Check for the existence of `conductor/setup_state.json`.
    - If it does not exist, this is a new project setup. Proceed directly to Step 2.0.
    - If it exists, read its content.

2.  **Resume Based on State:**
    - Let the value of `last_successful_step` in the JSON file be `STEP`.
    - Based on the value of `STEP`, jump to the **next logical section**:

    - If `STEP` is "2.1_product_guide", announce "Resuming setup: The Product Guide (`product.md`) is already complete. Next, we will create the Product Guidelines." and proceed to **Section 2.2**.
    - If `STEP` is "2.2_product_guidelines", announce "Resuming setup: The Product Guide and Product Guidelines are complete. Next, we will define the Technology Stack." and proceed to **Section 2.3**.
    - If `STEP` is "2.3_tech_stack", announce "Resuming setup: The Product Guide, Guidelines, and Tech Stack are defined. Next, we will select Code Styleguides." and proceed to **Section 2.4**.
    - If `STEP` is "2.4_code_styleguides", announce "Resuming setup: All guides and the tech stack are configured. Next, we will define the project workflow." and proceed to **Section 2.5**.
    - If `STEP` is "2.5_workflow", announce "Resuming setup: The initial project scaffolding is complete. Next, we will generate the first track." and proceed to **Phase 2 (3.0)**.
    - If `STEP` is "3.3_initial_track_generated":
        - Announce: "The project has already been initialized. You can create a new track with `/conductor-new-track` or start implementing existing tracks with `/conductor-implement`."
        - Halt the `setup` process.
    - If `STEP` is unrecognized, announce an error and halt.

---

## 2.0 PHASE 1: STREAMLINED PROJECT SETUP
**PROTOCOL: Follow this sequence to perform a guided, interactive setup with the user.**


### 2.0 Project Inception
1.  **Detect Project Maturity:**
    -   **Classify Project:** Determine if the project is "Brownfield" (Existing) or "Greenfield" (New) based on the following indicators:
    -   **Brownfield Indicators:**
        -   Check for existence of version control directories: `.git`, `.svn`, or `.hg`.
        -   If a `.git` directory exists, execute `git status --porcelain`. If the output is not empty, classify as "Brownfield" (dirty repository).
        -   Check for dependency manifests: `package.json`, `pom.xml`, `requirements.txt`, `go.mod`.
        -   Check for source code directories: `src/`, `app/`, `lib/` containing code files.
        -   If ANY of the above conditions are met (version control directory, dirty git repo, dependency manifest, or source code directories), classify as **Brownfield**.
    -   **Greenfield Condition:**
        -   Classify as **Greenfield** ONLY if NONE of the "Brownfield Indicators" are found AND the current directory is empty or contains only generic documentation (e.g., a single `README.md` file) without functional code or dependencies.

2.  **Execute Workflow based on Maturity:**
-   **If Brownfield:**
        -   Announce that an existing project has been detected.
        -   If the `git status --porcelain` command indicated uncommitted changes, inform the user: "WARNING: You have uncommitted changes in your Git repository. Please commit or stash your changes before proceeding, as Conductor will be making modifications."
        -   **Begin Brownfield Project Initialization Protocol:**
            -   **1.0 Pre-analysis Confirmation:**
                1.  **Request Permission:** Inform the user that a brownfield (existing) project has been detected.
                2.  **Ask for Permission:** Request permission for a read-only scan to analyze the project with the following options:
                    > A) Yes
                    > B) No
                3.  **Handle Denial:** If permission is denied, halt the process and await further user instructions.
                4.  **Confirmation:** Upon confirmation, proceed to the next step.

            -   **2.0 Code Analysis:**
                1.  **Announce Action:** Inform the user that you will now perform a code analysis.
                2.  **Prioritize README:** Begin by analyzing the `README.md` file, if it exists.
                3.  **Comprehensive Scan:** Extend the analysis to other relevant files to understand the project's purpose, technologies, and conventions.

            -   **2.1 File Size and Relevance Triage:**
                1.  **Respect Ignore Files:** Before scanning any files, you MUST check for the existence of `.geminiignore` and `.gitignore` files. If either or both exist, you MUST use their combined patterns to exclude files and directories from your analysis. The patterns in `.geminiignore` should take precedence over `.gitignore` if there are conflicts. This is the primary mechanism for avoiding token-heavy, irrelevant files like `node_modules`.
                2.  **Efficiently List Relevant Files:** To list the files for analysis, you MUST use a command that respects the ignore files. For example, you can use `git ls-files --exclude-standard -co | xargs -n 1 dirname | sort -u` which lists all relevant directories (tracked by Git, plus other non-ignored files) without listing every single file. If Git is not used, you must construct a `find` command that reads the ignore files and prunes the corresponding paths.
                3.  **Fallback to Manual Ignores:** ONLY if neither `.geminiignore` nor `.gitignore` exist, fall back to manually ignoring common directories. Example command: `ls -lR -I 'node_modules' -I '.m2' -I 'build' -I 'dist' -I 'bin' -I 'target' -I '.git' -I '.idea' -I '.vscode'`.
                4.  **Prioritize Key Files:** From the filtered list of files, focus your analysis on high-value, low-size files first, such as `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, and other configuration or manifest files.
                5.  **Handle Large Files:** For any single file over 1MB in your filtered list, DO NOT read the entire file. Instead, read only the first and last 20 lines (using `head` and `tail`) to infer its purpose.

            -   **2.2 Extract and Infer Project Context:**
                1.  **Strict File Access:** DO NOT ask for more files. Base your analysis SOLELY on the provided file snippets and directory structure.
                2.  **Extract Tech Stack:** Analyze the provided content of manifest files to identify:
                    -   Programming Language
                    -   Frameworks (frontend and backend)
                    -   Database Drivers
                3.  **Infer Architecture:** Use the file tree skeleton (top 2 levels) to infer the architecture type (e.g., Monorepo, Microservices, MVC).
                4.  **Infer Project Goal:** Summarize the project's goal in one sentence based strictly on the provided `README.md` header or `package.json` description.
        -   **Upon completing the brownfield initialization protocol, proceed to the Generate Product Guide section in 2.1.**
    -   **If Greenfield:**
        -   Announce that a new project will be initialized.
        -   Proceed to the next step.

3.  **Initialize Git Repository (for Greenfield):**
    -   If a `.git` directory does not exist, execute `git init` and report to the user.

4.  **Inquire about Project Goal (for Greenfield):**
    -   **Ask the user:** "What do you want to build?"
    -   **CRITICAL: Wait for the user's response before proceeding.**
    -   **Upon receiving the response:**
        -   Execute `mkdir -p conductor` (or equivalent).
        -   **Initialize State File:** Create `conductor/setup_state.json` with: `{"last_successful_step": ""}`
        -   Write the user's response into `conductor/product.md` under a header named `# Initial Concept`.

5.  **Continue:** Immediately proceed to the next section.

### 2.1 Generate Product Guide (Interactive)
1.  **Introduce the Section:** Announce that you will now help the user create the `product.md`.
2.  **Determine Mode:** Use the `ask_user` tool to let the user choose their preferred workflow.
    - **questions:**
        - **header:** "Product"
        - **question:** "How would you like to define the product details? Whether you prefer a quick start or a deep dive, both paths lead to a high-quality product guide!"
        - **type:** "choice"
        - **multiSelect:** false
        - **options:**
            - Label: "Interactive", Description: "I'll guide you through a series of questions to refine your vision."
            - Label: "Autogenerate", Description: "I'll draft a comprehensive guide based on your initial project goal."
        - **Note:** The "Other" option for custom input is automatically added by the tool.

3.  **Gather Information (Conditional):**
    -   **If user chose "Autogenerate":** Skip this step and proceed directly to **Step 4 (Draft the Document)**.
    -   **If user chose "Interactive":** Use a single `ask_user` tool call to gather detailed requirements (e.g., target users, goals, features).
        -   **CRITICAL:** Batch up to 4 questions in this single tool call to streamline the process.
        -   **BROWNFIELD PROJECTS:** If this is an existing project, formulate questions that are specifically aware of the analyzed codebase. Do not ask generic questions if the answer is already in the files.
        -   **SUGGESTIONS:** For each question, generate 3 high-quality suggested answers based on common patterns or context.
        -   **Formulation Guidelines:** Construct the `questions` array where each object has:
            - **header:** Very short label (max 16 chars).
            - **type:** "choice".
            - **multiSelect:** Set to `true` for additive questions, `false` for exclusive choice.
            - **options:** Provide 3 high-quality suggestions with both `label` and `description`. Do NOT include an "Autogenerate" option here.
            - **Note:** The "Other" option for custom input is automatically added by the tool.
        -   **Interaction Flow:** Wait for the user's response, then proceed to the next step.

4.  **Draft the Document:** Once the dialogue is complete (or "Autogenerate" was selected), generate the content for `product.md`.
    -   **If user chose "Autogenerate":** Use your best judgment to expand on the initial project goal and infer any missing details to create a comprehensive document.
    -   **If user chose "Interactive":** Use the specific answers provided. The source of truth is **only the user's selected answer(s)**. You are encouraged to expand on these choices to create a polished output.
5.  **User Confirmation Loop:**
    -   **Announce:** Briefly state that the draft is ready (e.g., "Draft generated."). Do NOT repeat the request to "review" or "approve" in the chat.
    -   **Ask for Approval:** Use the `ask_user` tool to request confirmation. You MUST embed the drafted content directly into the `question` field so the user can review it in context.
        - **questions:**
            - **header:** "Review"
            - **question:**
                Please review the drafted Product Guide below. What would you like to do next?

                ---

                <Insert Drafted product.md Content Here>
            - **type:** "choice"
            - **multiSelect:** false
            - **options:**
                - Label: "Approve", Description: "The product guide looks good, proceed."
                - Label: "Revise", Description: "I want to make some changes."
        - Await user feedback and revise the content until approved.
6.  **Write File:** Once approved, append to `conductor/product.md`, preserving `# Initial Concept`.
7.  **Commit State:** Write `conductor/setup_state.json`: `{"last_successful_step": "2.1_product_guide"}`
8.  **Continue:** Immediately proceed to next section.

### 2.2 Generate Product Guidelines (Interactive)
1.  **Introduce the Section:** Announce creation of `product-guidelines.md`.
2.  **Determine Mode:** Use the `ask_user` tool to let the user choose their preferred workflow.
    - **questions:**
        - **header:** "Guidelines"
        - **question:** "How would you like to define the product guidelines? You can provide quick guidance or dive deep into brand details!"
        - **type:** "choice"
        - **multiSelect:** false
        - **options:**
            - Label: "Interactive", Description: "I'll ask you targeted questions to establish the guidelines."
            - Label: "Autogenerate", Description: "I'll infer appropriate guidelines from the product definition and tech stack."
        - **Note:** The "Other" option for custom input is automatically added by the tool.

3.  **Gather Information (Conditional):**
    -   **If user chose "Autogenerate":** Skip this step and proceed directly to **Step 4 (Draft the Document)**.
    -   **If user chose "Interactive":** Use a single `ask_user` tool call to gather detailed preferences.
        -   **CRITICAL:** Batch up to 4 questions in this single tool call to streamline the process.
        -   **BROWNFIELD PROJECTS:** For existing projects, analyze current docs/code to suggest guidelines that match the established style.
        -   **SUGGESTIONS:** For each question, generate 3 high-quality suggested answers based on common patterns or context.
        -   **Formulation Guidelines:** Same as section 2.1.
            - **header:** Very short label (max 16 chars).
            - **type:** "choice".
            - **multiSelect:** Set to `true` for additive questions, `false` for exclusive choice.
            - **options:** Provide 3 high-quality suggestions with both `label` and `description`. Do NOT include an "Autogenerate" option here.
            - **Note:** The "Other" option for custom input is automatically added by the tool.
        -   **Interaction Flow:** Wait for the user's response, then proceed to the next step.

4.  **Draft the Document:** Once the dialogue is complete (or "Autogenerate" was selected), generate the content for `product-guidelines.md`.
    -   **If user chose "Autogenerate":** Use your best judgment to infer appropriate guidelines from the existing project context.
    -   **If user chose "Interactive":** Use the specific answers provided. The source of truth is **only the user's selected answer(s)**.
5.  **User Confirmation Loop:**
    -   **Announce:** Briefly state that the draft is ready. Do NOT repeat the request to "review" or "approve" in the chat.
    -   **Ask for Approval:** Use the `ask_user` tool to request confirmation. Embed the drafted content directly into the `question` field.
        - **questions:**
            - **header:** "Review"
            - **question:**
                Please review the drafted Product Guidelines below. What would you like to do next?

                ---

                <Insert Drafted product-guidelines.md Content Here>
            - **type:** "choice"
            - **multiSelect:** false
            - **options:**
                - Label: "Approve", Description: "The guidelines look good, proceed."
                - Label: "Revise", Description: "I want to make some changes."
        - Await user feedback and revise until approved.
6.  **Write File:** Write to `conductor/product-guidelines.md`.
7.  **Commit State:** `{"last_successful_step": "2.2_product_guidelines"}`
8.  **Continue.**

### 2.3 Generate Tech Stack (Interactive)
1.  **Introduce the Section:** Announce tech stack definition.
2.  **Determine Mode:** Use the `ask_user` tool to let the user choose their preferred workflow.
    - **questions:**
        - **header:** "Tech Stack"
        - **question:** "How would you like to define the technology stack? You can provide specific technologies or let me infer from your project context."
        - **type:** "choice"
        - **multiSelect:** false
        - **options:**
            - Label: "Interactive", Description: "I'll ask you specific questions about languages, frameworks, and tools."
            - Label: "Autogenerate", Description: "I'll analyze the project and infer the tech stack automatically."
        - **Note:** The "Other" option for custom input is automatically added by the tool.

3.  **Gather Information (Conditional):**
    -   **If user chose "Autogenerate":** Skip this step and proceed directly to **Step 4 (Draft the Document)**.
    -   **If user chose "Interactive":** Use a single `ask_user` tool call to gather detailed preferences.
        -   **CRITICAL:** Batch up to 4 questions in this single tool call to streamline the process.
        -   **BROWNFIELD PROJECTS:** If this is an existing project, state the inferred tech stack based on code analysis, then ask for confirmation (A: Yes / B: No). If "No", immediately ask for the correct stack using the same batched approach.
        -   **SUGGESTIONS:** For each question, generate 3 high-quality suggested answers based on common patterns or context.
        -   **Formulation Guidelines:** Same as section 2.1.
            - **header:** Very short label (max 16 chars).
            - **type:** "choice".
            - **multiSelect:** Set to `true` for additive questions (e.g., "Select all databases you're using"), `false` for exclusive choice.
            - **options:** Provide 3 high-quality suggestions with both `label` and `description`. Do NOT include an "Autogenerate" option here.
            - **Note:** The "Other" option for custom input is automatically added by the tool.
        -   **Interaction Flow:** Wait for the user's response, then proceed to the next step.

4.  **Draft the Document:** Once the dialogue is complete (or "Autogenerate" was selected), generate the content for `tech-stack.md`.
    -   **If user chose "Autogenerate":** Use your best judgment to infer the tech stack from the project files and create a comprehensive document.
    -   **If user chose "Interactive":** Use the specific answers provided. The source of truth is **only the user's selected answer(s)**.
5.  **User Confirmation Loop:**
    -   **Announce:** Briefly state that the draft is ready. Do NOT repeat the request to "review" or "approve" in the chat.
    -   **Ask for Approval:** Use the `ask_user` tool to request confirmation. Embed the drafted content directly into the `question` field.
        - **questions:**
            - **header:** "Review"
            - **question:**
                Please review the drafted Tech Stack below. What would you like to do next?

                ---

                <Insert Drafted tech-stack.md Content Here>
            - **type:** "choice"
            - **multiSelect:** false
            - **options:**
                - Label: "Approve", Description: "The tech stack looks correct."
                - Label: "Revise", Description: "I need to make adjustments."
        - Await user feedback and revise until approved.
6.  **Write File:** Write to `conductor/tech-stack.md`.
7.  **Commit State:** `{"last_successful_step": "2.3_tech_stack"}`
8.  **Continue.**

### 2.4 Select Guides (Interactive)
1.  **Initiate Dialogue:** Announce that style guides need selection.
2.  **Select Code Style Guides:**
    -   **Locate templates:** Find the `assets/code_styleguides/` directory relative to this SKILL.md. List the available style guide files.
    -   For new projects (greenfield):
        -   **Recommendation:** Based on Tech Stack, recommend appropriate style guide(s).
        -   Ask: A) Include recommended guides. B) Edit the selection.
        -   If editing: present all guides as numbered list and let user choose.
    -   For existing projects (brownfield):
        -   Announce inferred guides, ask for confirmation (A: Yes / B: Add more).
    -   **Action:** Create `conductor/code_styleguides/` and copy selected style guide files from the skill's `assets/code_styleguides/` directory.
    -   **Commit State:** `{"last_successful_step": "2.4_code_styleguides"}`

### 2.5 Select Workflow (Interactive)
1.  **Copy Initial Workflow:**
    -   Locate the `assets/workflow.md` template relative to this SKILL.md. Copy it to `conductor/workflow.md`.
    -   If template cannot be found, generate a default workflow.md with TDD methodology, >80% coverage, per-task commits, and git notes.
2.  **Customize Workflow:**
    -   Ask: "Do you want to use the default workflow or customize it?"
        -   A) Default
        -   B) Customize
    -   **If Default:** Keep as-is.
    -   **If Customize:**
        -   Q1: Coverage percentage (default 80%)
        -   Q2: Commit frequency (per task vs per phase)
        -   Q3: Git notes vs commit message for task summaries
        -   Update `conductor/workflow.md` based on responses.
3.  **Commit State:** `{"last_successful_step": "2.5_workflow"}`
4.  **CRITICAL: Immediately proceed to Section 2.6.**

### 2.6 Finalization

1.  **Generate Index File:**
    -   Create `conductor/index.md` with:
        ```markdown
        # Project Context

        ## Definition
        - [Product Definition](./product.md)
        - [Product Guidelines](./product-guidelines.md)
        - [Tech Stack](./tech-stack.md)

        ## Workflow
        - [Workflow](./workflow.md)
        - [Code Style Guides](./code_styleguides/)

        ## Management
        - [Tracks Registry](./tracks.md)
        - [Tracks Directory](./tracks/)
        ```

2.  **Immediately continue to Section 3.0.**

---

## 3.0 INITIAL PLAN AND TRACK GENERATION

### 3.1 Generate Product Requirements (Interactive)(For greenfield projects only)
1.  **Transition:** Read `conductor/product.md` and present the first requirement question.
2.  **Ask Questions Sequentially:** Max 5 questions with same guidelines.
    -   Last two options: "Type your own answer" and "Auto-generate the rest".
    -   **AUTO-GENERATE LOGIC:** Same as above.
3.  **Continue.**

### 3.2 Propose a Single Initial Track (Automated + Approval)
1.  **Generate and Present Track Title:** Analyze project context and present a single track.
    - Greenfield: Usually an MVP track.
    - Brownfield: Maintenance or enhancement track.
2.  **User Confirmation:** Get approval or ask for alternative.

### 3.3 Convert the Initial Track into Artifacts (Automated)
**CRITICAL: Once the track is approved, immediately begin creating ALL artifacts.**

1.  **Initialize Tracks File:** Create `conductor/tracks.md` with the first track entry.
2.  **Generate Track Artifacts:**
    a. Generate `spec.md` and `plan.md` for the track.
        - Plan MUST adhere to workflow principles (e.g., TDD sub-tasks).
        - Include `[ ]` status markers for every task and sub-task.
        - **Inject Phase Completion Tasks** if defined in workflow.
    b. Create Track ID (`shortname_YYYYMMDD`), directory, `metadata.json`, `spec.md`, `plan.md`, and `index.md`.
    c. **Commit State:** `{"last_successful_step": "3.3_initial_track_generated"}`

### 3.4 Final Announcement
1.  **Announce Completion.**
2.  **Save Conductor Files:** Commit all with `conductor(setup): Add conductor setup files`.
3.  **Next Steps:** Inform user to run `/conductor-implement`.
