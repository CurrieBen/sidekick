import os
import logging
import importlib
from django.conf import settings
from sidekick.services.helpers import update_task_status
from sidekick.models import Task

logger = logging.getLogger(__name__)


class CronTask:
    """Helpers for cron tasks """

    def __init__(self, task_name, registered_task_name, app):
        """
        Initialise variables and paths for CronTask class

        :param task_name: Name of task to run, will be displayed in lock files
        :param registered_task_name: Name of the registered task, used to update status
        :param app: Name of the app
        """
        if getattr(settings, "SIDEKICK")['LOCK_PATH']:
            self.app = app
            self.task_name = task_name
            self.registered_task_name = registered_task_name
            self.lock_path = settings.SIDEKICK['LOCK_PATH']
            self.lock_file = os.path.join(self.lock_path, '{}.lock'.format(self.task_name))
        else:
            print('missing sidekick settings for LOCK_PATH')

    def run(self):
        """Try to run management function.

        If lock file does not exist, run task, delete lock file.
        """
        if not self.lock_file_exists():
            self.create_lock_file()

            update_task_status(registered_task_name=self.registered_task_name, status=Task.IN_PROGRESS)
            try:
                app_task = self.app + '.tasks'
                importlib.import_module("%s" % app_task)
                # call the function using the getattr function
                getattr(importlib.import_module("%s" % app_task), self.task_name)()
                update_task_status(registered_task_name=self.registered_task_name, status=Task.SUCCESS)
                logger.info(msg='Successfully ran {}'.format(self.task_name))
            except Exception as e:
                update_task_status(registered_task_name=self.registered_task_name, status=Task.FAILED)
                logger.error(msg=e)
            self.delete_lock_file()

    def create_lock_file(self):
        """
        Create lock file before task is run at your specified path eg. /var/lock/project/task_name.lock
        """
        os.makedirs(self.lock_path, exist_ok=True)
        with open(self.lock_file, 'w+'):
            return False

    def delete_lock_file(self):
        """
        Delete lock file after task is run.
        """
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)

    def lock_file_exists(self):
        """Check if lock file exists for task.

        If it exists, notify us as that the task is starting again before finishing.
        Feel free to amend this and send yourself emails rather than logging

        :return: True if lock file exists
        """
        if os.path.isfile(self.lock_file):
            logger.info(msg="Lock file already exists for {} so the task did not run again".format(self.lock_file))
            return True
        return False
