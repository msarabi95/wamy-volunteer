# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import easy_thumbnails.fields
import userena.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'registered', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('ar_first_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0644')),
                ('ar_middle_name', models.CharField(max_length=30, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0623\u0628')),
                ('ar_last_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u062e\u064a\u0631')),
                ('en_first_name', models.CharField(max_length=30, verbose_name=b'First name')),
                ('en_middle_name', models.CharField(max_length=30, verbose_name=b'Middle name')),
                ('en_last_name', models.CharField(max_length=30, verbose_name=b'Last name')),
                ('mobile', models.CharField(max_length=30, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0648\u0627\u0644')),
                ('university', models.CharField(help_text='\u0627\u0633\u0645 \u0627\u0644\u062c\u0627\u0645\u0639\u0629 \u0643\u0627\u0645\u0644\u0627\u064b \u0628\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0639\u0631\u0628\u064a\u0629', max_length=128, verbose_name='\u0627\u0644\u062c\u0627\u0645\u0639\u0629')),
                ('academic_year', models.PositiveIntegerField(default=1, verbose_name='\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062f\u0631\u0627\u0633\u064a\u0629', choices=[(1, '\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u0623\u0648\u0644\u0649'), (2, '\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062b\u0627\u0646\u064a\u0629'), (3, '\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062b\u0627\u0644\u062b\u0629'), (4, '\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u0631\u0627\u0628\u0639\u0629'), (5, '\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062e\u0627\u0645\u0633\u0629'), (6, '\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u0633\u0627\u062f\u0633\u0629'), (7, '\u0633\u0646\u0629 \u0627\u0644\u0627\u0645\u062a\u064a\u0627\u0632')])),
                ('specialty', models.CharField(max_length=128, verbose_name='\u0627\u0644\u062a\u062e\u0635\u0635')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0645\u0644\u0641 \u0645\u0633\u062a\u062e\u062f\u0645',
                'verbose_name_plural': '\u0645\u0644\u0641\u0627\u062a \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u064a\u0646',
            },
            bases=(models.Model,),
        ),
    ]
