# Generated by Django 3.0.4 on 2020-03-15 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='genre',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.CharField(max_length=255),
        ),
    ]