from django.db import migrations


def do_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    CronSchedule = apps.get_model("sidekick", "CronSchedule")
    db_alias = schema_editor.connection.alias
    CronSchedule.objects.using(db_alias).bulk_create([
        CronSchedule(name="Every 5 minutes all day",
                     minute="*/5",
                     hour="*",
                     day_of_week="*",
                     day_of_month="*",
                     month_of_year="*"
                     ),
        CronSchedule(name="Every 10 minutes all day",
                     minute="*/10",
                     hour="*",
                     day_of_week="*",
                     day_of_month="*",
                     month_of_year="*"
                     ),
        CronSchedule(name="Every 15 minutes all day",
                     minute="*/15",
                     hour="*",
                     day_of_week="*",
                     day_of_month="*",
                     month_of_year="*"
                     ),
        CronSchedule(name="Every 30 minutes all day",
                     minute="*/30",
                     hour="*",
                     day_of_week="*",
                     day_of_month="*",
                     month_of_year="*"
                     ),
        CronSchedule(name="Every hour, all day",
                     minute="0",
                     hour="*",
                     day_of_week="*",
                     day_of_month="*",
                     month_of_year="*"
                     ),
        CronSchedule(name="At 5pm every day",
                     minute="0",
                     hour="17",
                     day_of_week="*",
                     day_of_month="*",
                     month_of_year="*"
                     )
    ])


def undo_func(apps, schema_editor):
    CronSchedule = apps.get_model("sidekick", "CronSchedule")
    db_alias = schema_editor.connection.alias
    CronSchedule.objects.using(db_alias).filter(name="Every 5 minutes all day").delete()
    CronSchedule.objects.using(db_alias).filter(name="Every 10 minutes all day").delete()
    CronSchedule.objects.using(db_alias).filter(name="Every 15 minutes all day").delete()
    CronSchedule.objects.using(db_alias).filter(name="Every 30 minutes all day").delete()
    CronSchedule.objects.using(db_alias).filter(name="Every hour, all day").delete()
    CronSchedule.objects.using(db_alias).filter(name="At 5pm every day").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('sidekick', '0001_initial')
    ]

    operations = [
        migrations.RunPython(do_func, undo_func),
    ]
