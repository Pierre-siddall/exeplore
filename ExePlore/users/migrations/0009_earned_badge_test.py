# Generated by Django 4.0.1 on 2022-03-01 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_player_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='earned_badge',
            name='test',
            field=models.CharField(default='test', max_length=10, verbose_name='Test'),
        ),
    ]