# Generated by Django 5.0.1 on 2024-03-28 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_alter_event_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='techgroup',
            name='icon',
            field=models.CharField(blank=True, help_text='Emojji or Font Awesome CSS icon class(es) to represent the group.', max_length=256),
        ),
    ]
