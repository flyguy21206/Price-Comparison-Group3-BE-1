# Generated by Django 3.2.4 on 2021-07-15 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='approved_comment',
            field=models.BooleanField(default=False),
        ),
    ]
