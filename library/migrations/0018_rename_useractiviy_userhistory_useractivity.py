# Generated by Django 3.2 on 2021-10-24 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_userhistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userhistory',
            old_name='useractiviy',
            new_name='useractivity',
        ),
    ]
