# Generated by Django 3.2.9 on 2021-11-06 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('room_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('user_name', models.CharField(max_length=255, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('tel', models.CharField(max_length=10)),
                ('isBanned', models.BooleanField(default=False)),
                ('pic', models.URLField(default='https://www.pngall.com/wp-content/uploads/5/User-Profile-PNG.png')),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('room_booked', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='room_api.room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
