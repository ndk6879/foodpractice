# Generated by Django 2.2.6 on 2019-11-14 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0008_auto_20191113_1053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='ingredient1',
            new_name='ingredient',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='ingredient2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='ingredient3',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='ingredient4',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='ingredient5',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='ingredient6',
        ),
    ]
