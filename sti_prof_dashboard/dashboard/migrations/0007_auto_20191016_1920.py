# Generated by Django 2.2.6 on 2019-10-16 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20191016_1911'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='is_dean',
            new_name='_is_dean',
        ),
    ]
