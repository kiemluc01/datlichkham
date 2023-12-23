# Generated by Django 5.0 on 2023-12-21 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.IntegerField(choices=[(1, 'ADMIN'), (2, 'CUSTOMER'), (3, 'DOCTOR')], default=2),
        ),
    ]
