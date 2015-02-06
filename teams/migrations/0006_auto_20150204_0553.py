# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20150204_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 4, 5, 53, 34, 13836, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 4, 5, 53, 38, 61634, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
