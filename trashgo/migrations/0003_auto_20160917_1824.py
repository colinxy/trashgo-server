# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trashgo', '0002_auto_20160917_0839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('frequency', models.IntegerField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trashgo.Team')),
            ],
        ),
        migrations.RemoveField(
            model_name='hotspot',
            name='team',
        ),
        migrations.AlterUniqueTogether(
            name='hotspot',
            unique_together=set([('longitude', 'latitude')]),
        ),
        migrations.AlterUniqueTogether(
            name='bin',
            unique_together=set([('longitude', 'latitude')]),
        ),
    ]
