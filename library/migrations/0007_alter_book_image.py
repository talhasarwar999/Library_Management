# Generated by Django 3.2 on 2021-09-29 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(default='', upload_to='librarymanage/images'),
        ),
    ]
