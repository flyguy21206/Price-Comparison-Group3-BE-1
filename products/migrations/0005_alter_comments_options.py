# Generated by Django 3.2.5 on 2021-07-05 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_comments_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['last_update'], 'verbose_name_plural': 'Comments'},
        ),
    ]
