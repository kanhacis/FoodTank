# Generated by Django 4.2.7 on 2023-11-29 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='house_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
