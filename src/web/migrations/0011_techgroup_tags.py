# Generated by Django 5.0.1 on 2024-05-30 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_eventbriteorganization'),
    ]

    operations = [
        migrations.AddField(
            model_name='techgroup',
            name='tags',
            field=models.ManyToManyField(blank=True, to='web.tag'),
        ),
    ]