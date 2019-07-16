import logging
from datetime import datetime, timezone

from django.db import models

logger = logging.getLogger(__name__)


class Task(models.Model):
    """Task model used to define tasks that will be run as cron jobs """

    FAILED = 'FAILED'
    IN_PROGRESS = 'IN_PROGRESS'
    SLEEPING = 'SLEEPING'
    SUCCESS = 'SUCCESS'

    CURRENT_STATUS = (
        (FAILED, 'Failed'),
        (IN_PROGRESS, 'In Progress'),
        (SLEEPING, 'Sleeping'),
        (SUCCESS, 'Success')
    )

    name = models.CharField(max_length=255, help_text='The human readable name of the task')
    registered_task = models.ForeignKey('sidekick.RegisteredTask', null=True, blank=True, on_delete=models.CASCADE)
    cron_schedule = models.ForeignKey('sidekick.CronSchedule', null=True, blank=True, on_delete=models.DO_NOTHING)
    enabled = models.BooleanField(default=False, help_text='Whether the task is enabled')
    status = models.CharField(max_length=11, choices=CURRENT_STATUS, default=SLEEPING)
    started_at = models.DateTimeField(null=True, blank=True, timezone=timezone.utc)
    finished_at = models.DateTimeField(null=True, blank=True, timezone=timezone.utc)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Task Pre Save"""
        if not self.registered_task or not self.cron_schedule:
            self.enabled = False

        super(Task, self).save(*args, **kwargs)

        """Task Post Save"""
        try:
            from sidekick.services.cron_files import CronService
            CronService().generate_cron_tasks()
        except Exception as e:
            logger.error(msg='Failed to generate cron task for {} due to {}'.format(self, e))

    def task_of(self):
        """The app which this task belongs to """
        return self.registered_task.task_name.split(' ')[0]

    def running_for(self):
        """How long has the current task been running for"""
        if self.status == self.IN_PROGRESS:
            now = datetime.now(timezone.utc)
            difference = now - self.started_at
            prefix = "Running for"
        elif self.started_at and self.finished_at:
            difference = self.finished_at - self.started_at
            prefix = "Completed in"
        else:
            return "Not currently running."
        days, seconds = difference.days, difference.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return "{} {} hours, {} minutes, {} seconds".format(prefix, hours, minutes, seconds)


class CronSchedule(models.Model):
    """Cron Schedule model for defining different time intervals """

    name = models.CharField(max_length=100, help_text='Human readable version of schedule, i.e Every 10 minutes')
    minute = models.CharField(max_length=100, help_text='At what minute. * for every', default='*')
    hour = models.CharField(max_length=100, help_text='At what hour. * for every', default='*')
    day_of_week = models.CharField(max_length=100, help_text='At what day of the week. * for every', default='*')
    day_of_month = models.CharField(max_length=100, help_text='At what day of the month. * for every', default='*')
    month_of_year = models.CharField(max_length=100, help_text='At what month of the year. * for every', default='*')

    def __str__(self):
        return self.name

    def schedule(self):
        return "{} {} {} {} {}".format(self.minute, self.hour, self.day_of_month, self.month_of_year, self.day_of_week)


class RegisteredTask(models.Model):
    """Model for the registered task to be used by the Task Model """

    task_name = models.CharField(max_length=125, help_text='The task to be run ie. stock --get_stock_updates')

    def __str__(self):
        return self.task_name.replace('--', ' - ').replace('_', ' ')
