# Generated by Django 3.2.15 on 2022-09-13 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_article_publish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='publish',
        ),
    ]