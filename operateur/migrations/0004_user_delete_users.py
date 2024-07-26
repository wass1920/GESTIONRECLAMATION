# Generated by Django 5.0.4 on 2024-04-29 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operateur', '0003_rename_user_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
