# Generated by Django 4.0 on 2021-12-28 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SecUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=20)),
                ('pic', models.FileField(blank=True, null=True, upload_to='profile')),
            ],
        ),
    ]
