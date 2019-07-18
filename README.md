# Side Kick

Side Kick is a simple, lightweight scheduler for Django management commands. Anything can be a management command, whether it is doing database back ups or sending emails. 
Simply create the task, add the decorator and then in Django's admin you can set when it should run and also enable or 
disable it. It will also make sure that the task will only run if there is no other instance of the task already running
to avoid unexpected issues if a task takes longer to complete than expected.


Installation:

``pip install side-kick``

Make sure you add ``sidekick`` to your installed apps.

Create a file somewhere within the project called ``tasks.txt``. The file can be wherever you want, as long as it is
inside the main project directory. This is where the tasks will be written to, which will be explained shortly.

Add the following to your settings file:

    SIDEKICK = {
        'SIDEKICK_REGISTERED_APPS': [],
        'ENVIRONMENT': "",
        'DJANGO_PATH': "",
        'CRON_PATH': "",
        'LOCK_PATH': ""
    }


``SIDEKICK_REGISTERED_APPS`` is where you will need to define all the apps which have tasks that sidekick will handle.
You just need to put the app name and then as soon as django loads it will import the tasks.py file of each app within
this list. Any tasks that have the ``@sidekick_task`` decorator will create a new RegisteredTask instance if it does
not already exist.

Each time you want to register a new task, don't forget to add it to this list.
``SIDEKICK_REGISTERED_APPS = ['stock', 'customers', 'pizzas',]``

``ENVIRONMENT`` is where you will define the user and the start-up file of that user for example:

    ENVIRONMENT = "root . /root/.profile"

`DJANGO_PATH` is the path to your project directory and then the path to python, followed by the manage.py command
which will be used to trigger the tasks. For example:

    DJANGO_PATH = "/var/www/myproject && /var/www/virtualenv/bin/python manage.py"


``CRON_PATH`` is the path to the tasks.txt file that you created earlier. This is where the cron files will be written,
so you can check within this file once you have registered a task that it is working correctly.

    CRON_PATH = "/var/www/myproject/sidekick_tasks/tasks.txt"


``LOCK_FILE`` is the path to a directory where the lock files will be created when a task starts running and then deleted
from when it is completed. The reason for this is to stop the same task running concurrently if the first instance of 
the task hasn't completed yet. This also can go anywhere but for ease of use I would suggest keeping it within the same
directory you choose to create the tasks.txt file.

    LOCK_PATH = "/var/www/myproject/sidekick_tasks/lock_files/"

These settings were designed so you can customise them and use different paths depending on the environment you are
working in etc.

Once this is done, you will need to migrate to create the side kick models which you can then manage 
through the django admin.

The basic set up is now complete!

When it comes to creating and registering tasks, follow these simple steps:

Add the ``@sidekick_task`` decorator to any tasks you wish to register, make sure the task is in your tasks.py file of your
app:

    from sidekick.decorators import sidekick_task

    @sidekick_task
    def my_task():
        # Whatever task you wish to complete
        ...

Then add the name of the app to the ``SIDEKICK_REGISTERED_APPS`` list in your settings file.

Create a new directory within the app called ``management`` and then a subdirectory called `commands`. Add a
``__init__.py`` file and then a file with the name of the app eg. ``customers.py`` to the ``commands`` directory.

If you already have management commands in this file, that is fine, you can skip this step, but make sure to add the 
code for ``add_arguments()`` and also ``handle()`` in the next step.

File structure would be as follows:

    myproject
    |_ customers
       |_management
         |_commands
            |_ __init__.py
            |_ customers.py

Within ``customers.py`` (or whatever your app is) add the following:


    import logging

    from django.core.management.base import BaseCommand
    from sidekick.services.helpers import get_task_name, get_app_name
    from sidekick.services.crontab import CronTask

    from sidekick.models import RegisteredTask

    logger = logging.getLogger(__name__)
    app_name = get_app_name(__name__)


    class Command(BaseCommand):
        help = "Commands for the Stock app"

        def add_arguments(self, parser):
            """Defines the arguments """

            for task in RegisteredTask.objects.filter(task_name__startswith=app_name):
                task_name = task.task_name.split(' ')[1]
                parser.add_argument(
                    task_name,
                    action='store_true',
                    dest=task_name[2:]
                )

        def handle(self, *args, **options):
            """Handle stock management commands.

            :param args:
            :param options: Arguments passed with command e.g. send_emails_to_customers, verbosity etc.
            """
            task_name = get_task_name(options)
            rt_task_name = "{} --{}".format(app_name, task_name)

            if RegisteredTask.objects.filter(task_name=rt_task_name):
                try:
                    CronTask(task_name=task_name, registered_task_name=rt_task_name, app=app_name).run()
                except Exception as e:
                    logger.error(msg=e)


You will need to have this same file structure in each app you want to have tasks registered to.
 
Once this is done, you need to create a file within the ``/etc/cron.d`` directory called anything you like, I would
suggest something like ``sidekick_tasks``, and then create a sym link between this file and the tasks.txt file you
created earlier.

You can do this by connecting to your server and then:

    cd /etc/cron.d
    touch sidekick_tasks
    ln -sf /var/www/myproject/path/to/tasks.txt /etc/cron.d/sidekick_tasks
    
Once this is done then you're all good to go, you can now register tasks with a simple decorator and easily 
manage them using django admin.


![Side Kick Admin Example](./sidekick/static/images/SideKickAdmin.png?raw=true "Side Kick Admin Example")
