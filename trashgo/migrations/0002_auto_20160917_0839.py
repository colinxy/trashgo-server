# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 08:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trashgo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('RED', 'Team Red'), ('BLUE', 'Team Blue'), ('YELLOW', 'Team Yellow')], default='RED', max_length=10)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='location',
            name='user',
        ),
        migrations.AlterField(
            model_name='user',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trashgo.Team'),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.AddField(
            model_name='hotspot',
            name='team',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='trashgo.Team'),
            preserve_default=False,
        ),
    ]
