# Generated by Django 4.0.6 on 2022-08-23 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_user_age_alter_user_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
