# Generated by Django 3.2.7 on 2021-09-03 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210903_1628'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='Week',
            new_name='week',
        ),
    ]
