# Generated by Django 4.0 on 2022-03-24 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay',
            name='payid',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
