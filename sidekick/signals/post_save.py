import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from sidekick.models import Task
from sidekick.services.cron_files import CronService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Task)
def task_post_save(sender, instance, **kwargs):
    """Methods to be run on the post save of the Task model """
    try:
        CronService().generate_cron_tasks()
    except Exception as e:
        logger.error(msg='Failed to generate cron task for {} due to {}'.format(instance, e))
