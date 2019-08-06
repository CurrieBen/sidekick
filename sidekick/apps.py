from django.apps import AppConfig
from django.conf import settings


class SidekickConfig(AppConfig):
    name = 'sidekick'

    def ready(self):
        self.register_tasks()

    @staticmethod
    def register_tasks():
        """
        For each app listed in SIDEKICK_REGISTERED_APPS import the task to trigger the decorator
        :return:
        """
        import importlib
        try:
            for app in settings.SIDEKICK['SIDEKICK_REGISTERED_APPS']:
                app_task = app + '.tasks'
                importlib.import_module("%s" % app_task)
        except Exception as e:
            print("Failed to register tasks for Side Kick. Make sure you have SIDEKICK_REGISTERED_APPS within"
                  " the SIDEKICK dictionary.")

    @staticmethod
    def clean_up_old_lock_files():
        """
        If the server has just been restarted, check if there are any old lock files and if so remove them
        :return:
        """
        import os
        from .models import RegisteredTask

        for task in RegisteredTask.objects.all():
            lock_path = settings.SIDEKICK['LOCK_PATH']
            lock_file_name = "{name}.lock".format(name=task.task_name.split("--")[1])
            path = os.path.join(lock_path, lock_file_name)
            if os.path.exists(path):
                os.remove(path)
