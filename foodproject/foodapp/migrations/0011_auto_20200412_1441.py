# Generated by Django 2.2.6 on 2020-04-12 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0010_menu_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='ingredient',
            new_name='Essential_ingredient',
        ),
    ]
