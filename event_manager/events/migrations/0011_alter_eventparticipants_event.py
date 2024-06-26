# Generated by Django 4.2.10 on 2024-04-17 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0010_eventparticipants_notified_alter_event_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventparticipants",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="events.event",
                verbose_name="мероприятие",
            ),
        ),
    ]
