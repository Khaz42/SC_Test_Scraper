# Generated by Django 3.0.4 on 2020-03-15 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20200315_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]