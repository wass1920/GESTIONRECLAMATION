# Generated by Django 5.0.4 on 2024-04-29 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operateur', '0002_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Users',
        ),
    ]
