# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '\u0637\u0644\u0628', 'verbose_name_plural': '\u0627\u0644\u0637\u0644\u0628\u0627\u062a'},
        ),
        migrations.AlterField(
            model_name='code',
            name='category',
            field=models.ForeignKey(related_name='codes', verbose_name='\u0627\u0644\u0641\u0626\u0629', to='codes.Category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='code',
            name='event',
            field=models.ForeignKey(related_name='codes', verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', to='teams.Event'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='code',
            name='order',
            field=models.ForeignKey(related_name='codes', verbose_name='\u0627\u0644\u0637\u0644\u0628', to='codes.Order'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='code',
            name='user',
            field=models.ForeignKey(related_name='redeemed_codes', verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='event',
            field=models.ForeignKey(related_name='code_orders', verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', to='teams.Event'),
            preserve_default=True,
        ),
    ]
