# Generated by Django 3.1.4 on 2021-01-10 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0007_auto_20210110_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn_number',
            field=models.CharField(blank=True, max_length=13, unique=True),
        ),
    ]