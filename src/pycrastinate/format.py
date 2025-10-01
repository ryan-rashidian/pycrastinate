"""Rich style and formatting for terminal output."""

from datetime import datetime

from rich.console import Console
from rich.text import Text
from rich.theme import Theme

from .tasks import Task

custom_themes = Theme({
    'main': 'orange1',
    'alternate': 'light_goldenrod2',
    'info': 'navajo_white1',
    'high': 'red',
    'medium': 'light_goldenrod1',
    'low': 'dark_olive_green3',
    'warning': 'bold red'
})

console = Console(theme=custom_themes)

def _color_task(task: Task, theme: str) -> tuple[Text, Text, Text, Text]:
    """Give color theme to task."""
    id_fmt = Text(task.id, style=theme)
    date_fmt = Text(task.date, style=theme)
    description_fmt = Text(task.description, style='info')
    status_fmt = Text(task.status, style='alternate')
    return status_fmt, id_fmt, description_fmt, date_fmt

def style_task(task: Task) -> tuple[Text, Text, Text, Text]:
    """Style task text based on due date."""
    now = datetime.now().date()

    if now < task.task_date.date():
        return _color_task(task, 'low')
    elif now == task.task_date.date():
        return _color_task(task, 'medium')
    else:
        return _color_task(task, 'high')

