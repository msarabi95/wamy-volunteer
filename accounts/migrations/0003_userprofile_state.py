# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.ForeignKey(related_name='user_profiles', default=1, verbose_name='\u0627\u0644\u0645\u0646\u0637\u0642\u0629', to='accounts.State'),
            preserve_default=False,
        ),
    ]
