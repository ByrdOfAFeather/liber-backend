# Generated by Django 3.1.4 on 2020-12-28 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0004_auto_20201228_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='olid',
            field=models.TextField(null=True, unique=True),
        ),
    ]
