# Generated by Django 3.2.16 on 2023-03-17 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20230317_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image_name',
            new_name='image',
        ),
    ]
