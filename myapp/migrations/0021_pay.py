# Generated by Django 4.0 on 2022-03-24 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_alter_notice_ntime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pamount', models.IntegerField()),
                ('ptime', models.DateTimeField(auto_now_add=True)),
                ('pdate', models.DateField()),
                ('pverifiy', models.BooleanField(default=False)),
                ('payid', models.CharField(max_length=50)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.addmember')),
            ],
        ),
    ]
