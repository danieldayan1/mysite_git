# Generated by Django 4.0.6 on 2022-08-23 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_alter_user_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='url',
            field=models.URLField(default=None),
        ),
    ]
