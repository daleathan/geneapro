# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-13 15:55
from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    Theme = apps.get_model('geneaprove', 'Theme')
    Rule = apps.get_model('geneaprove', 'Rule')
    RulePart = apps.get_model('geneaprove', 'RulePart')

    theme = Theme.objects.create(name='Custom Theme Demo')
    theme.save()

    rule = theme.rules.create(
        name='', type='default', sequence_number=0,
        style_fill='#dcf4dc', style_color='#000000',
        style_stroke='#f62500', style_font_weight='normal')
    rule.save()

    rule = theme.rules.create(
        name='Persons that are still alive',
        type='alive',
        sequence_number=1,
        style_fill='#97ee53')
    rule.save()
    rule.parts.create(field='alive', operator='=bool', value='True')

    rule = theme.rules.create(
        name='Persons not born in France',
        type='event',
        sequence_number=2,
        style_fill='#efa990')
    rule.save()
    rule.parts.create(field='typ', operator='=int', value='9')
    rule.parts.create(field='role', operator='=int', value='1')
    rule.parts.create(field='place_name', operator='!icontains', value='france')

    rule = theme.rules.create(
        name='Person died young',
        type='event',
        sequence_number=3,
        style_fill='#f32847')
    rule.save()
    rule.parts.create(field='typ', operator='=int', value='18')
    rule.parts.create(field='role', operator='=int', value='1')
    rule.parts.create(field='age', operator='<=int', value='56')

    rule = theme.rules.create(
        name='Person appears multiple times in tree of currently selected person',
        type='implex',
        sequence_number=4,
        style_fill='#fbfc57')
    rule.save()
    rule.parts.create(field='ref', operator='=pers', value='-1')
    rule.parts.create(field='count', operator='>=int', value='2')

    rule = theme.rules.create(
        name='All male ancestors of person 2',
        type='and',
        sequence_number=5,
        style_font_weight='bold')
    rule.save()

    child = rule.children.create(
        name='', type='characteristic', sequence_number=0, theme=theme)
    child.save()
    child.parts.create(field='typ', operator='=int', value='29')
    child.parts.create(field='value', operator='=', value='M')

    child = rule.children.create(
        name='', type='ancestor', sequence_number=1, theme=theme)
    child.save()
    child.parts.create(field='ref', operator='=pers', value='2')

    rule = theme.rules.create(
        name='People without a known father',
        type='knownfather',
        sequence_number=6,
        style_fill='#cdb1fc')
    rule.save()
    rule.parts.create(field='known', operator='=bool', value='false')

    rule = theme.rules.create(
        name='Born or dead in Paris before 1910',
        type='event',
        sequence_number=7,
        style_fill='#abf5fd')
    rule.save()
    rule.parts.create(field='typ', operator='in_int', value='[9, 18]')
    rule.parts.create(field='place_name', operator='icontains', value='paris')
    rule.parts.create(field='date', operator='<str', value='1910-01-01')
    rule.parts.create(field='role', operator='=int', value='1')

    rule = theme.rules.create(
        name='Persons whose name is Dauve',
        type='characteristic',
        sequence_number=8,
        style_stroke='#55e819')
    rule.save()
    rule.parts.create(field='typ', operator='=int', value='39')
    rule.parts.create(field='value', operator='i=', value='dauve')

    rule = theme.rules.create(
        name='Persons married more than once',
        type='event',
        sequence_number=9,
        style_color='#f53145')
    rule.save()
    rule.parts.create(field='typ', operator='=int', value='28')
    rule.parts.create(field='count', operator='>int', value='1')
    rule.parts.create(field='role', operator='=int', value='1')

    rule = theme.rules.create(
        name='Warning: person too young at birth of child',
        type='event',
        sequence_number=10,
        style_fill='#f4491a')
    rule.save()
    rule.parts.create(field='typ', operator='=int', value='9')
    rule.parts.create(field='role', operator='in_int', value='[2,3]')
    rule.parts.create(field='age', operator='<int', value='17')

    theme.save()


class Migration(migrations.Migration):

    dependencies = [
        ('geneaprove', '0006_themes'),
    ]

    operations = [
        migrations.RunPython(forward),
    ]
