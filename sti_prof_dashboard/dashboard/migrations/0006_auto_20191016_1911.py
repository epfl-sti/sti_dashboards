# Generated by Django 2.2.6 on 2019-10-16 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20191016_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='managed_institutes',
            new_name='_managed_institutes',
        ),
    ]
