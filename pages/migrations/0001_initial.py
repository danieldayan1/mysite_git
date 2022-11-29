# Generated by Django 4.0.6 on 2022-08-23 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=8, unique=True)),
                ('mail', models.EmailField(max_length=254)),
                ('tel', models.CharField(max_length=11)),
                ('age', models.IntegerField()),
                ('url', models.URLField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
