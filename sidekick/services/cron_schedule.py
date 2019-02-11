import logging
from sidekick.models import Task

logger = logging.getLogger(__name__)


class CronScheduleService:
    """
    Services for the cron schedule
    """
    @staticmethod
    def handle_removing_schedule(schedule_instance):
        """
        If a cron schedule is deleted then make sure you mark any tasks that were using it as no longer enabled
        :return:
        """
        logger.info(msg="Pre Delete of CronSchedule instance - disabling tasks with this cron schedule")
        tasks = Task.objects.filter(cron_schedule=schedule_instance)
        # noinspection PyBroadException
        try:
            for task in tasks:
                task.enabled = False
                task.save()
                logger.info(msg="{} has been disabled due to no longer having a cron schedule associated to it".format(
                    task
                ))
        except Exception:
            logger.error(msg="Failed during process of disabling sidekick tasks on pre_delete of a cron schedule")
