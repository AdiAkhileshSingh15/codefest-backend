# Generated by Django 2.2.17 on 2023-10-01 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arithmetica', '0003_auto_20231002_0306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='errorinfo',
            old_name='user',
            new_name='user_info',
        ),
        migrations.AlterUniqueTogether(
            name='errorinfo',
            unique_together={('user_info', 'round')},
        ),
    ]
