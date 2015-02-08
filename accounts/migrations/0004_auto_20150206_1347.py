# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.ForeignKey(related_name='user_profiles', verbose_name='\u0627\u0644\u0645\u0646\u0637\u0642\u0629', to='accounts.State', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='university',
            field=models.CharField(max_length=128, verbose_name='\u0627\u0644\u062c\u0627\u0645\u0639\u0629'),
            preserve_default=True,
        ),
    ]
