# Generated by Django 4.1.5 on 2023-01-05 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InstanceName', models.CharField(max_length=255)),
                ('HostName', models.CharField(max_length=255)),
                ('PrimaryIpAddress', models.CharField(max_length=255)),
                ('OSName', models.CharField(max_length=255)),
                ('InstanceTypeFamily', models.CharField(max_length=255)),
                ('Cpu', models.IntegerField()),
                ('Memory', models.IntegerField()),
                ('Status', models.CharField(max_length=255)),
                ('InstanceBandwidthRx', models.IntegerField()),
                ('VSwitchID', models.CharField(max_length=255)),
                ('SecurityGroupId', models.TextField()),
                ('Lastseen', models.DateTimeField(verbose_name='date de mise en ligne')),
            ],
        ),
    ]
