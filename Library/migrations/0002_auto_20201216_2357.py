# Generated by Django 3.1.4 on 2020-12-16 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='full_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='publisher',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]
