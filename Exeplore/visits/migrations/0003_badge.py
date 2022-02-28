# Generated by Django 4.0.1 on 2022-02-28 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0002_alter_location_latitude_alter_location_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=300)),
                ('tier', models.CharField(choices=[('PT', 'Platinum'), ('AU', 'Gold'), ('AG', 'Silver'), ('BR', 'Bronze')], default='BR', max_length=2)),
            ],
        ),
    ]
