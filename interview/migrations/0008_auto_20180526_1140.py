# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-05-26 09:40
from __future__ import unicode_literals

from django.db import migrations

from interview.models import Process as P2

def process_save(process):
    process.save()

    if process.state in ('WA',
                      'WK',
                      'JO'):
        process.responsible.clear()
        if process.subsidiary.responsible:
            process.responsible.add(process.subsidiary.responsible)
    if process.state in ('CD', 'HI'):
        process.responsible.clear()
    if process.state in ('WP',
                      'WI'):
        process.responsible.clear()
        for interviewer in process.interview_set.last().interviewers.all():
            process.responsible.add(interviewer)

    if process.state not in P2.CLOSED_STATE_VALUES:
        for interview in process.interview_set.exclude(state__in=['GO', 'NO']):
            for interviewer in interview.interviewers.all():
                process.responsible.add(interviewer)

def migrate_state(apps, schema_editor):
    Interview = apps.get_model('interview', 'Interview')
    Process = apps.get_model('interview', 'Process')

    for i in Interview.objects.all():
        is_new = i.id is None

        if i.rank is None:
            # Rank is based on the number of interviews during the
            # same process that occured before the interview
            i.rank = (Interview.objects.filter(process=i.process).values_list('rank', flat=True).last() or 0) + 1

        if is_new:
            i.state = 'NP'

        if i.planned_date is None and i.state is None:
            i.state = 'NP'
        else:
            if i.state == 'NP' and i.planned_date is not None:
                i.state = 'PL'

        if is_new or (Interview.objects.filter(process=i.process).last() == i and i.process.state not in P2.CLOSED_STATE_VALUES):
            if i.state == 'NP':
                i.process.state = 'WP'
                process_save(i.process)
            elif i.state == 'PL':
                i.process.state = 'WI'
                process_save(i.process)
            if i.state in ('GO', 'NO'):
                i.process.state = 'WK'
                process_save(i.process)

        i.save()

    for p in Process.objects.all():
        process_save(p)

    for p in Process.objects.filter(state='OP'):
        if p.interview_set.count():
            p.state = 'WK'
            process_save(p)
        else:
            p.state = 'WA'
            process_save(p)


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0007_auto_20180526_0944'),
    ]

    operations = [
        migrations.RunPython(migrate_state),
    ]
