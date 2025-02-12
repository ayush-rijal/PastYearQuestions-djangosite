# Generated by Django 5.0.6 on 2024-08-30 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_profile_email_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrafficData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('total_visits', models.IntegerField(default=0)),
                ('unique_visitors', models.IntegerField(default=0)),
            ],
        ),
    ]
