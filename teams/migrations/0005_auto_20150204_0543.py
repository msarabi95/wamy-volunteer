# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20150204_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 4, 5, 43, 40, 193673, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='evaluation',
            unique_together=set([('event', 'user')]),
        ),
    ]
