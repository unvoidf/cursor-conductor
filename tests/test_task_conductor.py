import sys
import os
from pathlib import Path

# Add .cursor/hooks to sys.path to import task_conductor
repo_root = Path(__file__).resolve().parent.parent
hooks_dir = repo_root / ".cursor" / "hooks"
sys.path.append(str(hooks_dir))

import task_conductor

def test_count_tasks_empty():
    """Test with empty string."""
    assert task_conductor.count_tasks("") == {
        "pending": 0, "in_progress": 0, "completed": 0, "skipped": 0
    }

def test_count_tasks_single_types():
    """Test each task type individually."""
    assert task_conductor.count_tasks("- [ ] Pending Task")["pending"] == 1
    assert task_conductor.count_tasks("- [~] In Progress Task")["in_progress"] == 1
    assert task_conductor.count_tasks("- [x] Completed Task")["completed"] == 1
    assert task_conductor.count_tasks("- [-] Skipped Task")["skipped"] == 1

def test_count_tasks_mixed():
    """Test with mixed task types."""
    plan = """
- [ ] Pending 1
- [~] In Progress 1
- [x] Completed 1
- [-] Skipped 1
- [ ] Pending 2
    """
    counts = task_conductor.count_tasks(plan)
    assert counts["pending"] == 2
    assert counts["in_progress"] == 1
    assert counts["completed"] == 1
    assert counts["skipped"] == 1

def test_count_tasks_whitespace():
    """Test whitespace handling."""
    plan = """
    - [ ] Indented Pending
      - [~] Indented In Progress
- [x] Completed No Indent
    """
    counts = task_conductor.count_tasks(plan)
    assert counts["pending"] == 1
    assert counts["in_progress"] == 1
    assert counts["completed"] == 1

def test_count_tasks_invalid_lines():
    """Test lines that should be ignored."""
    plan = """
This is a header
- Not a task
[ ] Missing dash
- [ ]No space
-[ ] No space after dash
    """
    counts = task_conductor.count_tasks(plan)
    assert counts["pending"] == 0
    assert counts["in_progress"] == 0
    assert counts["completed"] == 0
    assert counts["skipped"] == 0

def test_count_tasks_bold_content():
    """Test task with bold content."""
    plan = "- [ ] **Bold Task**"
    counts = task_conductor.count_tasks(plan)
    assert counts["pending"] == 1

def test_count_tasks_empty_description():
    """Test tasks with empty descriptions."""
    # Current implementation uses strip(), so '- [ ] ' becomes '- [ ]'
    # and fails startswith('- [ ] ').
    # Tasks must have at least one non-whitespace character after the brackets.
    plan = """
- [ ]
- [ ]
- [ ] .
    """
    counts = task_conductor.count_tasks(plan)
    # The first two lines are stripped to '- [ ]' and don't match '- [ ] '
    # The third line is stripped to '- [ ] .' and matches.
    assert counts["pending"] == 1
