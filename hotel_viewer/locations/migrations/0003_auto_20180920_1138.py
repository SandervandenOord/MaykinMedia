# Generated by Django 2.1.1 on 2018-09-20 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20180920_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='city_id',
            new_name='city',
        ),
    ]
