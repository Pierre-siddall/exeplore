# Generated by Django 4.0.1 on 2022-03-01 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0004_badge_icon'),
        ('users', '0002_alter_player_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='badges',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='visits.badge', verbose_name='Badges'),
        ),
        migrations.AlterField(
            model_name='player',
            name='visits',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='visits.location', verbose_name='Visits'),
        ),
    ]
