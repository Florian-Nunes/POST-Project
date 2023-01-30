# Generated by Django 4.1.5 on 2023-01-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ETL', '0002_alter_ecs_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='slb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SLBName', models.CharField(max_length=255)),
                ('SLBId', models.CharField(max_length=255)),
                ('SLBIp', models.CharField(max_length=255)),
                ('SLBPort', models.IntegerField()),
                ('SLBEnvironment', models.CharField(max_length=255)),
                ('SLBProtocol', models.CharField(max_length=255)),
                ('SLBNetworkType', models.CharField(max_length=255)),
                ('SLBAlgorithm', models.IntegerField()),
                ('SLBStatus', models.CharField(max_length=255)),
                ('Lastseen', models.DateTimeField(verbose_name='date de mise en ligne')),
            ],
            options={
                'verbose_name': 'Slb',
                'verbose_name_plural': 'Slb',
            },
        ),
    ]