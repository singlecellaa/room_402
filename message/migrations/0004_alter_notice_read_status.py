# Generated by Django 4.2.10 on 2024-02-27 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_alter_notice_shared_people_alter_notice_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='read_status',
            field=models.BooleanField(default=False, verbose_name='阅读状态'),
        ),
    ]