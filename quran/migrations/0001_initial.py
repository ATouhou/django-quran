# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 04:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttext', models.TextField(blank=True, db_index=True, null=True)),
                ('utext', models.TextField(blank=True, db_index=True, null=True)),
                ('number', models.IntegerField(verbose_name='Aya Number')),
                ('bismillah', models.CharField(blank=True, max_length=50, verbose_name='Bismillah')),
            ],
            options={
                'ordering': ['sura', 'number'],
            },
        ),
        migrations.CreateModel(
            name='AyaTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttext', models.TextField()),
                ('aya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='quran.Aya')),
            ],
            options={
                'ordering': ['aya'],
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Definite',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lemma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttext', models.TextField(blank=True, db_index=True, null=True)),
                ('utext', models.TextField(blank=True, db_index=True, null=True)),
                ('meaning', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['ttext'],
            },
        ),
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Other',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Participle',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pos',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Root',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttext', models.TextField(blank=True, db_index=True, null=True)),
                ('utext', models.TextField(blank=True, db_index=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttext', models.TextField(blank=True, db_index=True, null=True)),
                ('utext', models.TextField(blank=True, db_index=True, null=True)),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Case')),
                ('definite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Definite')),
                ('form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Form')),
                ('gender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Gender')),
                ('lemma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='segments', to='quran.Lemma')),
                ('mood', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Mood')),
                ('other', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Other')),
                ('participle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Participle')),
                ('pos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Pos')),
            ],
            options={
                'ordering': ['ttext'],
            },
        ),
        migrations.CreateModel(
            name='Special',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sura',
            fields=[
                ('ttext', models.TextField(blank=True, db_index=True, null=True)),
                ('utext', models.TextField(blank=True, db_index=True, null=True)),
                ('etext', models.TextField(blank=True, db_index=True, null=True)),
                ('number', models.IntegerField(primary_key=True, serialize=False, verbose_name='Sura Number')),
                ('order', models.IntegerField(verbose_name='Revelation Order')),
                ('type', models.CharField(choices=[('Meccan', 'Meccan'), ('Medinan', 'Medinan')], max_length=7, verbose_name='')),
                ('rukus', models.IntegerField(verbose_name='Number of Rukus')),
                ('aya_count', models.IntegerField()),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Tense',
            fields=[
                ('ttext', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttext', models.CharField(max_length=50)),
                ('translator', models.CharField(max_length=50)),
                ('source_name', models.CharField(max_length=50)),
                ('source_url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttext', models.TextField(blank=True, db_index=True, null=True)),
                ('utext', models.TextField(blank=True, db_index=True, null=True)),
                ('number', models.IntegerField()),
                ('aya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='quran.Aya')),
                ('sura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='quran.Sura')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='WordSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('type', models.CharField(max_length=10)),
                ('segment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_segments', to='quran.Segment')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_segments', to='quran.Word')),
            ],
        ),
        migrations.AddField(
            model_name='segment',
            name='special',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Special'),
        ),
        migrations.AddField(
            model_name='segment',
            name='tense',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quran.Tense'),
        ),
        migrations.AddField(
            model_name='segment',
            name='words',
            field=models.ManyToManyField(related_name='segments', through='quran.WordSegment', to='quran.Word'),
        ),
        migrations.AddField(
            model_name='lemma',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lemmas', to='quran.Root'),
        ),
        migrations.AddField(
            model_name='ayatranslation',
            name='sura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='quran.Sura'),
        ),
        migrations.AddField(
            model_name='ayatranslation',
            name='translation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quran.Translation'),
        ),
        migrations.AddField(
            model_name='aya',
            name='sura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ayas', to='quran.Sura'),
        ),
        migrations.AlterUniqueTogether(
            name='word',
            unique_together=set([('aya', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='ayatranslation',
            unique_together=set([('aya', 'translation')]),
        ),
        migrations.AlterUniqueTogether(
            name='aya',
            unique_together=set([('number', 'sura')]),
        ),
    ]
