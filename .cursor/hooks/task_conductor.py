#!/usr/bin/env python3
"""
Conductor stop Hook for Cursor Agent CLI.

This hook runs when the agent loop ends. It checks whether the agent
was executing a Conductor implementation task, reads the track's plan.md
to determine if there are remaining tasks, and sends a followup_message
to continue autonomous execution if needed.
"""

import json
import sys
import os
import re
from pathlib import Path


def find_active_track_plan(conductor_dir: Path) -> Path | None:
    """Find the plan.md of the currently in-progress track."""
    tracks_file = conductor_dir / "tracks.md"
    if not tracks_file.exists():
        return None

    try:
        content = tracks_file.read_text(encoding="utf-8")
    except Exception:
        return None

    # Find in-progress track link
    # Pattern: - [~] **Track: ...** \n *Link: [./tracks/track_id/](./tracks/track_id/)*
    sections = content.split("---")
    for section in sections:
        if "[~]" in section and "**Track:" in section:
            # Extract link path
            link_match = re.search(r'\[([^\]]+/)\]\(([^\)]+)\)', section)
            if link_match:
                relative_path = link_match.group(2).rstrip("/")
                plan_path = conductor_dir.parent / relative_path.lstrip("./") / "plan.md"
                if plan_path.exists():
                    return plan_path

    # Fallback: search tracks directory
    tracks_dir = conductor_dir / "tracks"
    if tracks_dir.exists():
        for track_dir in sorted(tracks_dir.iterdir(), reverse=True):
            if track_dir.is_dir():
                plan = track_dir / "plan.md"
                metadata = track_dir / "metadata.json"
                if plan.exists() and metadata.exists():
                    try:
                        meta = json.loads(metadata.read_text(encoding="utf-8"))
                        if meta.get("status") in ("in_progress", "new"):
                            return plan
                    except Exception:
                        continue

    return None


def count_tasks(plan_content: str) -> dict:
    """Count task statuses in a plan.md file."""
    counts = {
        "pending": 0,       # [ ]
        "in_progress": 0,   # [~]
        "completed": 0,     # [x]
        "skipped": 0,       # [-]
    }

    for line in plan_content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- [ ] "):
            counts["pending"] += 1
        elif stripped.startswith("- [~] "):
            counts["in_progress"] += 1
        elif stripped.startswith("- [x] "):
            counts["completed"] += 1
        elif stripped.startswith("- [-] "):
            counts["skipped"] += 1

    return counts


def get_next_pending_task(plan_content: str) -> str | None:
    """Get the description of the next pending task."""
    for line in plan_content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- [ ] Task:") or stripped.startswith("- [ ] **Task:"):
            # Extract task name
            task = stripped.replace("- [ ] Task:", "").replace("- [ ] **Task:", "").strip()
            task = task.rstrip("*").strip()
            return task
    return None


def main():
    # Read the hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, Exception) as e:
        sys.stderr.write(f"[conductor] task_conductor: Failed to parse input: {e}\n")
        print("{}")
        sys.exit(0)

    status = input_data.get("status", "")
    loop_count = input_data.get("loop_count", 0)

    # Only process completed agent runs
    if status != "completed":
        print("{}")
        sys.exit(0)

    # Check if conductor mode is active
    conductor_active = os.environ.get("CONDUCTOR_ACTIVE", "false")
    if conductor_active != "true":
        print("{}")
        sys.exit(0)

    # Get project directory
    project_dir = Path(os.environ.get("CURSOR_PROJECT_DIR", "."))
    conductor_dir = project_dir / "conductor"

    if not conductor_dir.exists():
        print("{}")
        sys.exit(0)

    # Find the active track's plan
    plan_path = find_active_track_plan(conductor_dir)
    if not plan_path:
        print("{}")
        sys.exit(0)

    # Read and analyze the plan
    try:
        plan_content = plan_path.read_text(encoding="utf-8")
    except Exception:
        print("{}")
        sys.exit(0)

    counts = count_tasks(plan_content)
    next_task = get_next_pending_task(plan_content)

    # If there are pending tasks, send a followup message
    if counts["pending"] > 0 and next_task:
        total = counts["pending"] + counts["in_progress"] + counts["completed"] + counts["skipped"]
        done = counts["completed"] + counts["skipped"]
        progress = f"{done}/{total}"

        # Also check transcript for conductor-implement context
        transcript_path = input_data.get("transcript_path")
        is_implement_session = False
        if transcript_path and os.path.exists(transcript_path):
            try:
                with open(transcript_path, "r", encoding="utf-8") as f:
                    # Read last portion of transcript to check for conductor context
                    f.seek(max(0, os.path.getsize(transcript_path) - 8192))
                    transcript_tail = f.read()
                    if "conductor-implement" in transcript_tail.lower() or \
                       "conductor workflow" in transcript_tail.lower() or \
                       "plan.md" in transcript_tail:
                        is_implement_session = True
            except Exception:
                pass

        if is_implement_session:
            followup = (
                f"Continue implementing the track. Progress: {progress} tasks done. "
                f"Next task: \"{next_task}\". "
                f"Follow the Conductor workflow: read the task from plan.md, "
                f"mark it [~], implement following the workflow (TDD if applicable), "
                f"commit, record SHA, mark [x], then move to the next task."
            )
            response = {"followup_message": followup}
            print(json.dumps(response, ensure_ascii=False))
            sys.exit(0)

    # No followup needed
    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
