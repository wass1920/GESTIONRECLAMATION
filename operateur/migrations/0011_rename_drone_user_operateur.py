# Generated by Django 5.0.4 on 2024-05-01 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operateur', '0010_user_drone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='drone',
            new_name='operateur',
        ),
    ]
