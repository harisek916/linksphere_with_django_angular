# Generated by Django 5.0.6 on 2024-06-11 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_userprofile_block_alter_userprofile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
