# Generated by Django 4.2.10 on 2024-04-11 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_alter_event_is_canceled_alter_event_is_private"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventparticipants",
            name="status",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Обязательно буду"), (1, "Пока решаю"), (2, "Не пойду")],
                default=1,
                verbose_name="статус",
            ),
        ),
    ]
