# Generated by Django 4.0.4 on 2022-08-30 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_portfolio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algorithm_id', models.IntegerField()),
                ('creation_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('finish', models.BooleanField(default=False)),
            ],
        ),
    ]
