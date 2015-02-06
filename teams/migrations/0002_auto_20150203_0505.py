# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CriterionResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response', models.PositiveIntegerField(verbose_name='\u0627\u0644\u062a\u0642\u064a\u064a\u0645')),
            ],
            options={
                'verbose_name': '\u062a\u0642\u064a\u064a\u0645 \u0641\u0631\u0639\u064a',
                'verbose_name_plural': '\u0627\u0644\u062a\u0642\u064a\u064a\u0645\u0627\u062a \u0627\u0644\u0641\u0631\u0639\u064a\u0629',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', to='teams.Event')),
                ('user', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u062a\u0642\u064a\u064a\u0645',
                'verbose_name_plural': '\u0627\u0644\u062a\u0642\u064a\u064a\u0645\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EvaluationCriterion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0646\u0635')),
                ('max_score', models.PositiveIntegerField(default=5, verbose_name='\u0627\u0644\u062d\u062f \u0627\u0644\u0623\u0642\u0635\u0649')),
            ],
            options={
                'verbose_name': '\u0645\u0639\u064a\u0627\u0631 \u062a\u0642\u064a\u064a\u0645',
                'verbose_name_plural': '\u0645\u0639\u0627\u064a\u064a\u0631 \u0627\u0644\u062a\u0642\u064a\u064a\u0645',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='criterionresponse',
            name='criterion',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0639\u064a\u0627\u0631', to='teams.EvaluationCriterion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='criterionresponse',
            name='evaluation',
            field=models.ForeignKey(to='teams.Evaluation'),
            preserve_default=True,
        ),
    ]
