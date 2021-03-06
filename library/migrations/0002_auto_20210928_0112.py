# Generated by Django 3.2 on 2021-09-28 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='signup',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='signup',
            name='passwords',
        ),
        migrations.RemoveField(
            model_name='signup',
            name='phno',
        ),
        migrations.AddField(
            model_name='signup',
            name='confirm_passwords',
            field=models.CharField(default=1, max_length=31),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signup',
            name='email',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signup',
            name='role_select',
            field=models.CharField(default=2, max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='signup',
            name='password',
            field=models.CharField(max_length=30),
        ),
    ]
