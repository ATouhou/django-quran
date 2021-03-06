# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 23:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quran', '0004_auto_20160526_0538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wordmeaning',
            old_name='word_number',
            new_name='number',
        ),
        migrations.RemoveField(
            model_name='wordmeaning',
            name='aya_number',
        ),
        migrations.RemoveField(
            model_name='wordmeaning',
            name='sura_number',
        ),
        migrations.AddField(
            model_name='wordmeaning',
            name='aya',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='word_meanings', to='quran.Aya'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wordmeaning',
            name='sura',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='word_meanings', to='quran.Sura'),
            preserve_default=False,
        ),
    ]
