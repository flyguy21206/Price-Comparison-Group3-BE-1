# Generated by Django 3.2.4 on 2021-07-16 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_comments_approved_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='amazon_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='product',
            name='ebay_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
