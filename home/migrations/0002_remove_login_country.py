# Generated by Django 4.0.3 on 2022-04-14 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='login',
            name='country',
        ),
    ]
