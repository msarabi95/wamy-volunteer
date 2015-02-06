# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
            ],
            options={
                'verbose_name': '\u0645\u0646\u0637\u0642\u0629',
                'verbose_name_plural': '\u0627\u0644\u0645\u0646\u0627\u0637\u0642',
            },
            bases=(models.Model,),
        ),
    ]
