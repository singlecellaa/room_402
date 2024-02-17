# Generated by Django 4.2 on 2024-02-15 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='room_app.club'),
        ),
        migrations.AlterField(
            model_name='user',
            name='depart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='room_app.depart'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, '使用者'), (2, '管理员')], null=True),
        ),
    ]
