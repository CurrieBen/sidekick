"""
Helper functions to make the code quicker to write and easier for others to read
"""


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
