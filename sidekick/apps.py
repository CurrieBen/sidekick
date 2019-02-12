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
