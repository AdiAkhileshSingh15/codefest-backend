# Generated by Django 2.2.17 on 2023-10-01 21:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arithmetica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoundInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('problem_statement', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ErrorInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error', models.FloatField(default=30.0, validators=[django.core.validators.MinValueValidator(0)])),
                ('submitted_function', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arithmetica.RoundInfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'round')},
            },
        ),
    ]
