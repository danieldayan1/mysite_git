# Generated by Django 4.0.6 on 2022-08-23 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_alter_user_age_alter_user_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mail',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
