#!/usr/bin/env python3
"""
Conductor sessionStart Hook for Cursor Agent CLI.

This hook runs at the beginning of every new composer conversation.
It detects whether the project uses the Conductor workflow by checking
for the conductor/ directory and index.md file, then injects relevant
context into the session.
"""

import json
import sys
import os
from pathlib import Path


def main():
    # Read the hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"[conductor] session_init: Failed to parse input: {e}\n")
        print(json.dumps({"continue": True}))
        sys.exit(0)

    # Get the project directory
    project_dir = Path(os.environ.get("CURSOR_PROJECT_DIR", "."))

    response = {
        "continue": True,
        "env": {},
        "additional_context": ""
    }

    # Check if conductor/ directory exists
    conductor_dir = project_dir / "conductor"
    index_file = conductor_dir / "index.md"

    if not conductor_dir.exists():
        # No conductor setup - pass through silently
        response["env"]["CONDUCTOR_ACTIVE"] = "false"
        print(json.dumps(response, ensure_ascii=False))
        sys.exit(0)

    # Conductor is present - activate conductor mode
    response["env"]["CONDUCTOR_ACTIVE"] = "true"
    response["env"]["CONDUCTOR_DIR"] = str(conductor_dir.resolve())

    # Build additional context
    context_parts = []
    context_parts.append(
        "## Conductor Project Detected\n"
        "This project uses the **Conductor** workflow framework for context-driven development.\n"
        "The `conductor/` directory contains the project's product definition, tech stack, "
        "workflow, and track-based implementation plans.\n"
    )

    # Read index.md if it exists
    if index_file.exists():
        try:
            index_content = index_file.read_text(encoding="utf-8")
            context_parts.append(
                "### Project Index (`conductor/index.md`)\n"
                f"{index_content}\n"
            )
        except Exception:
            pass

    # Check for active tracks
    tracks_file = conductor_dir / "tracks.md"
    if tracks_file.exists():
        try:
            tracks_content = tracks_file.read_text(encoding="utf-8")
            # Count track statuses
            pending = tracks_content.count("- [ ] **Track:")
            in_progress = tracks_content.count("- [~] **Track:")
            completed = tracks_content.count("- [x] **Track:")

            response["env"]["CONDUCTOR_TRACKS_PENDING"] = str(pending)
            response["env"]["CONDUCTOR_TRACKS_IN_PROGRESS"] = str(in_progress)
            response["env"]["CONDUCTOR_TRACKS_COMPLETED"] = str(completed)

            if in_progress > 0:
                context_parts.append(
                    f"### Active Tracks\n"
                    f"There are **{in_progress} track(s) in progress**, "
                    f"{pending} pending, and {completed} completed.\n"
                    f"The user can invoke `/conductor-implement` to continue working "
                    f"on the current track, or `/conductor-status` to see detailed progress.\n"
                )
            elif pending > 0:
                context_parts.append(
                    f"### Track Status\n"
                    f"There are **{pending} pending track(s)** ready for implementation.\n"
                    f"The user can invoke `/conductor-implement` to start working.\n"
                )
        except Exception:
            pass

    # Provide available conductor commands
    context_parts.append(
        "### Available Conductor Commands\n"
        "- `/conductor-setup` - Initialize or resume project setup\n"
        "- `/conductor-new-track` - Create a new track (feature/bug/chore)\n"
        "- `/conductor-implement` - Execute tasks from the current track's plan\n"
        "- `/conductor-status` - Show project progress overview\n"
        "- `/conductor-review` - Review completed work against guidelines\n"
        "- `/conductor-revert` - Git-aware revert of tracks/phases/tasks\n"
    )

    response["additional_context"] = "\n".join(context_parts)

    print(json.dumps(response, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
