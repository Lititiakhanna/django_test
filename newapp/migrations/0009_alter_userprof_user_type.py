# Generated by Django 3.2.15 on 2022-08-28 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0008_alter_userprof_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprof',
            name='user_type',
            field=models.CharField(max_length=20),
        ),
    ]
