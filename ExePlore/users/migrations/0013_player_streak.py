# Generated by Django 4.0.1 on 2022-03-22 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_rename_earned_badge_earnedbadge'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='streak',
            field=models.IntegerField(default=0, verbose_name='Streak'),
        ),
    ]
