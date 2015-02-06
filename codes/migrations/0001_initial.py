# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('credit', models.FloatField(verbose_name='\u0639\u062f\u062f \u0627\u0644\u0633\u0627\u0639\u0627\u062a')),
            ],
            options={
                'verbose_name': '\u0641\u0626\u0629',
                'verbose_name_plural': '\u0627\u0644\u0641\u0626\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.CharField(unique=True, max_length=16, verbose_name='\u0627\u0644\u0646\u0635')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0646\u0634\u0627\u0621')),
                ('date_redeemed', models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0627\u0633\u062a\u062e\u062f\u0627\u0645', blank=True)),
                ('date_downloaded', models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u062d\u0645\u064a\u0644', blank=True)),
                ('category', models.ForeignKey(verbose_name='\u0627\u0644\u0641\u0626\u0629', to='codes.Category')),
                ('event', models.ForeignKey(verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', to='teams.Event')),
            ],
            options={
                'verbose_name': '\u0631\u0645\u0632',
                'verbose_name_plural': '\u0627\u0644\u0631\u0645\u0648\u0632',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0646\u0634\u0627\u0621')),
                ('event', models.ForeignKey(verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', to='teams.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='code',
            name='order',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0637\u0644\u0628', to='codes.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='code',
            name='user',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
