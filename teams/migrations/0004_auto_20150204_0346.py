# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20150203_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterionresponse',
            name='evaluation',
            field=models.ForeignKey(related_name='criterion_responses', to='teams.Evaluation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='event',
            field=models.ForeignKey(related_name='evaluations', verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', to='teams.Event'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(related_name='evaluations', verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluationcriterion',
            name='description',
            field=models.CharField(help_text='\u0627\u0644\u0633\u0624\u0627\u0644 \u0627\u0644\u0630\u064a \u0633\u064a\u0638\u0647\u0631 \u0644\u0645\u0646 \u0633\u064a\u0642\u0648\u0645 \u0628\u0627\u0644\u062a\u0642\u064a\u064a\u0645.', max_length=128, verbose_name='\u0627\u0644\u0648\u0635\u0641'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluationcriterion',
            name='max_score',
            field=models.PositiveIntegerField(default=5, help_text='\u0645\u0639\u064a\u0627\u0631 \u0627\u0644\u062a\u0642\u064a\u064a\u0645 \u0639\u0628\u0627\u0631\u0629 \u0639\u0646 \u0633\u0644\u0645 \u0645\u0646 \u0661 \u0625\u0644\u0649 \u0627\u0644\u062d\u062f \u0627\u0644\u0623\u0642\u0635\u0649 \u0627\u0644\u0630\u064a \u064a\u062a\u0645 \u062a\u062d\u062f\u064a\u062f\u0647.', verbose_name='\u0627\u0644\u062d\u062f \u0627\u0644\u0623\u0642\u0635\u0649'),
            preserve_default=True,
        ),
    ]
