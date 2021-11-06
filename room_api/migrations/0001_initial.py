# Generated by Django 3.2.9 on 2021-11-06 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=1)),
                ('max_price', models.IntegerField()),
                ('min_price', models.IntegerField()),
                ('type_name', models.CharField(max_length=20)),
                ('room_free', models.IntegerField()),
                ('rating', models.FloatField()),
                ('pic', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_num', models.IntegerField()),
                ('price', models.IntegerField()),
                ('person_per_room', models.CharField(max_length=10)),
                ('detail', models.TextField()),
                ('pic', models.URLField()),
                ('isFree', models.BooleanField(default=True)),
                ('exp_date', models.DurationField(blank=True, null=True)),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_api.roomtype')),
            ],
        ),
    ]
