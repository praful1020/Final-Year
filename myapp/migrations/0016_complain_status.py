# Generated by Django 4.0 on 2022-02-02 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_rename_pic_complain_cpic'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
