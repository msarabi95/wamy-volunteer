# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20150203_0505'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationcriterion',
            name='description',
            field=models.CharField(default='', max_length=128, verbose_name='\u0627\u0644\u0648\u0635\u0641'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluationcriterion',
            name='label',
            field=models.CharField(max_length=128, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646'),
            preserve_default=True,
        ),
    ]
