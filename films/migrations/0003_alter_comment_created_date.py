# Generated by Django 4.2.1 on 2023-06-24 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_alter_comment_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
