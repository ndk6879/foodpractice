# Generated by Django 2.2.6 on 2019-11-11 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0006_auto_20191111_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='ingredient1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='ingredient2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='ingredient3',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='ingredient4',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
