# Generated by Django 2.2.6 on 2019-11-13 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0007_auto_20191111_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='ingredient1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='ingredient2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='ingredient3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='ingredient4',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='ingredient5',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='ingredient6',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
