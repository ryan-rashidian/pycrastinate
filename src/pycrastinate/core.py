"""Contains core logic for orchestrating application workflow."""

from datetime import datetime

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from pycrastinate.format import console, style_task
from pycrastinate.tasks import Task, load_json, save_json


def menu_prompt_options() -> None:
    """Options menu."""
    main_prompt = (
        '[A]dd | '
        '[C]omplete | '
        '[R]emove | '
        '[S]ave | '
        '[V]iew | '
        '[Q]uit'
    )
    panel = Panel(
        Text(main_prompt, style='alternate'),
        title='Options',
        padding=1,
        style='main'
    )
    console.print(panel, justify='center')

def prompt_task_description() -> str | None:
    """Prompt user for task description."""
    console.print(
        Text('>>> (Enter Description | [C]ancel): '),
        style = 'main',
        end = ''
    )
    desc_input = input()
    return desc_input if desc_input.upper() != 'C' else None

def prompt_task_date() -> str | None:
    """Prompt user for task date."""
    while True:
        console.print(
            Text('>>> (Enter Date [YYYY-MM-DD] | [C]ancel): '),
            style = 'main',
            end = ''
        )
        date_input = input().strip()
        try:
            if date_input.upper() == 'C':
                return None
            datetime.fromisoformat(date_input)
            return date_input
        except ValueError:
            console.print(Text(f'Incorrect Format: {date_input}'))

def get_unique_id(tasks: list[Task]) -> int:
    """Calculate unique id value."""
    task_ids = [task.task_id for task in tasks]
    try:
        return max(task_ids) + 1
    except ValueError:
        return 1

def render_tasks(tasks: list[Task]) -> None:
    """Generate Table of current tasks."""
    sorted_tasks = sorted(tasks, key=lambda t: t.task_date)

    table = Table(box=box.ROUNDED, expand=True, style='main')
    table.add_column(
        Text('[\u2713]', style='alternate'),
        justify='center',
        ratio=1
    )
    table.add_column(
        Text('ID', style='alternate'),
        justify='center',
        ratio=1
    )
    table.add_column(
        Text('Description', style='alternate'),
        justify='left',
        ratio=6
    )
    table.add_column(
        Text('Date', style='alternate'),
        justify='center',
        ratio=2
    )

    for task in sorted_tasks:
        table.add_row(*style_task(task))

    console.print(Panel(table, title='PyCrastinate', border_style='main'))

class PyCrastinate:
    """Main orchestrator class for PyCrastinate CLI loop."""

    def __init__(self):
        """Initialize saved tasks."""
        self.running = False
        self.tasks = [Task(id=id, **task) for id, task in load_json().items()]

    def _save_tasks(self) -> None:
        """Save current task list."""
        save_json({task.id: task.to_dict() for task in self.tasks})

    def _exit_loop(self) -> None:
        """Exit PyCal CLI loop."""
        self.running = False

    def _add_task(self) -> None:
        """Add task to list."""
        description = prompt_task_description()
        if not description:
            return
        date = prompt_task_date()
        if not date:
            return
        id = get_unique_id(self.tasks)

        self.tasks.append(Task(
            id = str(id),
            description = description,
            date = date
        ))

    def _remove_task(self, cmd: str) -> None:
        """Remove task from list."""
        for task in self.tasks:
            if cmd == task.id:
                self.tasks.remove(task)

    def _complete_task(self, cmd: str) -> None:
        """Mark a task finished or un-finished."""
        for task in self.tasks:
            if cmd == task.id:
                task.complete()

    def _handle_commands(self, user_cmd: str):
        """Handle user input during CLI loop."""
        if user_cmd == 'A':
            self._add_task()
        elif user_cmd in ('C', 'R'):
            console.print(
                Text('>>> (Enter task ID | [C]ancel): '),
                end = ''
            )
            task_id_input = input().strip()
            if task_id_input.upper() != 'C':
                match user_cmd:
                    case 'C':
                        self._complete_task(task_id_input)
                    case 'R':
                        self._remove_task(task_id_input)
        elif user_cmd == 'S':
            self._save_tasks()
        elif user_cmd == 'Q':
            self._exit_loop()

    def run_loop(self) -> None:
        """Start PyCrastinate CLI loop."""
        self.running = True

        while self.running:
            console.clear()
            render_tasks(self.tasks)
            menu_prompt_options()

            console.print(Text('>>> ', style='main'), end='')
            user_cmd = input().strip().upper()
            self._handle_commands(user_cmd)

