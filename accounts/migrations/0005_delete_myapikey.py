# Generated by Django 5.0 on 2023-12-28 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_myapikey'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyAPIKey',
        ),
    ]