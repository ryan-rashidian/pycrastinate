"""Task loading and saving."""

import json
from dataclasses import dataclass
from datetime import datetime

from pycrastinate._paths import TASK_PATH


@dataclass
class Task:
    """PyCrastinate task container."""
    id: str
    description: str
    date: str
    status: str = '[ ]'

    @property
    def task_id(self) -> int:
        return int(self.id)

    @property
    def task_date(self) -> datetime:
        return datetime.fromisoformat(self.date)

    def complete(self) -> None:
        """Mark task as complete."""
        self.status = '[\u2713]'

    def to_dict(self) -> dict:
        """Convert Task to dictionary intermediate for saving to JSON."""
        return {
            'description': self.description,
            'date': self.date,
            'status': self.status
        }

def load_json() -> dict:
    """Load from tasks JSON."""
    try:
        with open(TASK_PATH, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_json(tasks: dict):
    """Save to tasks JSON."""
    with open(TASK_PATH, 'w') as f:
        json.dump(tasks, f, indent=2)

