# Generated by Django 4.1.1 on 2022-09-29 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0004_room_category"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room",
            old_name="toillets",
            new_name="toilets",
        ),
    ]