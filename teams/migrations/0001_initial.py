# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
            ],
            options={
                'verbose_name': '\u0646\u0634\u0627\u0637',
                'verbose_name_plural': '\u0627\u0644\u0623\u0646\u0634\u0637\u0629',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
            ],
            options={
                'verbose_name': '\u0641\u0631\u064a\u0642',
                'verbose_name_plural': '\u0627\u0644\u0641\u0631\u0642',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='team',
            field=models.ForeignKey(related_name='events', verbose_name='\u0627\u0644\u0641\u0631\u064a\u0642', to='teams.Team'),
            preserve_default=True,
        ),
    ]
