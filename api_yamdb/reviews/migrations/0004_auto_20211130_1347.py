# Generated by Django 2.2.16 on 2021-11-30 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_user_is_staff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_bio',
            new_name='bio',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_role',
            new_name='role',
        ),
    ]
