# Generated by Django 2.2.15 on 2020-08-17 17:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0002_auto_20200817_1734'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Lists',
            new_name='List',
        ),
    ]
