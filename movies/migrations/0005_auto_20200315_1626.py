# Generated by Django 3.0.4 on 2020-03-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20200315_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='average_note',
            field=models.FloatField(null=True),
        ),
    ]
