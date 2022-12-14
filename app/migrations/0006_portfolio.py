# Generated by Django 4.0.4 on 2022-08-29 16:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_delete_gini_protofilo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('risk', models.IntegerField()),
                ('algorithm_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('creation_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
