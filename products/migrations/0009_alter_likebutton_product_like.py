# Generated by Django 3.2.2 on 2021-08-01 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_likebutton_product_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likebutton',
            name='product_like',
            field=models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='Like', max_length=7),
        ),
    ]
