# Generated by Django 3.2.7 on 2021-10-01 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_choice_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='test',
        ),
    ]