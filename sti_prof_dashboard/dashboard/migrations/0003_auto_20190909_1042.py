# Generated by Django 2.2.1 on 2019-09-09 08:42

from django.db import migrations
import url_or_relative_url_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20190909_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='picture_url',
            field=url_or_relative_url_field.fields.URLOrRelativeURLField(blank=True, default=None, null=True),
        ),
    ]
