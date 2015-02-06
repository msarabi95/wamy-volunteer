# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0002_auto_20150119_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='short_link',
            field=models.URLField(null=True, verbose_name='\u0631\u0627\u0628\u0637 \u0642\u0635\u064a\u0631', blank=True),
            preserve_default=True,
        ),
    ]
