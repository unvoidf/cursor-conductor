# Cursor Conductor

> **Ported from:** [`gemini-cli-extensions/conductor`]
---

## 🚀 What is Cursor Conductor?

Cursor Conductor brings the power of **Context-Driven Development** to Cursor IDE's Agent CLI. It's a direct port of the [Gemini CLI Conductor extension](https://github.com/gemini-cli-extensions/conductor) — adapted specifically for Cursor.

✨ **Measure twice, code once.** ✨

Instead of just writing code, Conductor makes your AI agent a proactive project manager that follows a strict protocol: **Context → Spec → Plan → Implement**.

---

## ⚡ Quick Setup

### 1️⃣ Clone & Copy

```bash
# Clone this repository
git clone https://github.com/unvoidf/cursor-conductor.git

# Copy the .cursor folder to your project root
cp -r cursor-conductor/.cursor/ /path/to/your/project/
```

### 2️⃣ Restart Cursor

**Important:** If Cursor is running while you copy the `.cursor` folder, **restart Cursor** completely. This ensures the new skills and hooks are loaded properly.

---

## 💬 Commands at a Glance

| Command | Purpose |
|---------|---------|
| `/conductor-setup` | 🏗️ Initialize project context (product, tech stack, workflow) |
| `/conductor-new-track` | 📝 Create new feature/bug with interactive spec & plan |
| `/conductor-implement` | ⚙️ Auto-execute tasks from plan (autonomous mode) |
| `/conductor-status` | 📊 View project progress overview |
| `/conductor-review` | 🔍 Review work against guidelines |
| `/conductor-revert` | ↩️ Smart Git revert (tracks, phases, tasks) |

## 📁 Project Structure

After running `/conductor-setup`, your project will include:

```
your-project/
├── .cursor/                    # <-- You add this from this repo
│   ├── skills/                 # Conductor command skills
│   ├── hooks/                  # Automation scripts (Python)
│   └── hooks.json              # Hook configuration
├── conductor/                  # <-- Created by setup
│   ├── product.md
│   ├── product-guidelines.md
│   ├── tech-stack.md
│   ├── workflow.md
│   ├── code_styleguides/
│   ├── tracks.md               # Track registry
│   └── tracks/
│       └── <track_id>/
│           ├── spec.md
│           ├── plan.md
│           └── metadata.json
└── ... your source code
```

---

## 🔧 Requirements

- **Cursor IDE** with Agent CLI support
- **Python 3.8+** (for hook scripts)
- **Git** (for version control integration)

---

Made with ❤️ for the Cursor community. Ported from the awesome work by the Gemini CLI extensions team.
