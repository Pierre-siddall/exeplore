# Generated by Django 4.0.1 on 2022-03-01 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0004_badge_icon'),
        ('users', '0006_player_badges_player_visits'),
    ]

    operations = [
        migrations.CreateModel(
            name='Earned_Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_earned_datetime', models.DateTimeField(auto_now_add=True, verbose_name='datetime earned')),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visits.badge')),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_datetime', models.DateTimeField(auto_now_add=True, verbose_name='datetime visited')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visits.location')),
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='badges',
        ),
        migrations.AddField(
            model_name='player',
            name='badges',
            field=models.ManyToManyField(through='users.Earned_Badge', to='visits.Badge', verbose_name='Badges'),
        ),
        migrations.RemoveField(
            model_name='player',
            name='visits',
        ),
        migrations.AddField(
            model_name='player',
            name='visits',
            field=models.ManyToManyField(through='users.Visit', to='visits.Location', verbose_name='Visits'),
        ),
        migrations.AddField(
            model_name='visit',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.player'),
        ),
        migrations.AddField(
            model_name='earned_badge',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.player'),
        ),
    ]
