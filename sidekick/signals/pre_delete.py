import logging

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from sidekick.models import CronSchedule
from sidekick.services.cron_schedule import CronScheduleService

logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=CronSchedule)
def cron_schedule_pre_delete(sender, instance, **kwargs):
    """Methods to be run on the pre delete of a CronSchedule """
    # noinspection PyBroadException
    try:
        CronScheduleService.handle_removing_schedule(instance)
    except Exception:
        logger.error(msg="Failed during cron schedule pre delete")
