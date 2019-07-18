"""
Helper functions to make the code quicker to write and easier for others to read
"""
from datetime import datetime, timezone
from sidekick.models import Task


def get_task_name(options):
    """
    Given a dictionary of command options, return the name of the task
    :param options: Options passed to the handle method of the management command
    :return: The task name (str)
    """
    options_dict = dict(options)
    return [task for task in [key for key in options_dict] if str(options_dict[task]) == 'True'][0]


def get_app_name(name):
    """
    Given the __name__ return the app name
    :param name: __name__
    :return: App name
    """
    return name.split('.')[-1]


def update_task_status(registered_task_name, status):
    """Update the status, started_at and finished_at fields"""

    if status == Task.IN_PROGRESS:
        Task.objects.filter(registered_task__task_name=registered_task_name).update(
            status=status, started_at=datetime.now(timezone.utc))
    elif status in {Task.SUCCESS, Task.FAILED}:
        Task.objects.filter(registered_task__task_name=registered_task_name).update(
            status=status, finished_at=datetime.now(timezone.utc))
    else:
        Task.objects.filter(registered_task__task_name=registered_task_name).update(
            status=status, started_at=None, finished_at=None)
