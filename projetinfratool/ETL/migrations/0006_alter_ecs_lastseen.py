# Generated by Django 4.1.5 on 2023-01-10 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ETL', '0005_alter_slb_lastseen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecs',
            name='Lastseen',
            field=models.DateTimeField(),
        ),
    ]
