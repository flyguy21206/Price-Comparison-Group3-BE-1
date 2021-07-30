# Generated by Django 3.2.4 on 2021-07-30 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=512, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('amazon_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ebay_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('amazon_url', models.URLField(blank=True, default=None, null=True)),
                ('ebay_url', models.URLField(blank=True, default=None, null=True)),
                ('amazon_asin', models.CharField(blank=True, default=None, max_length=12, null=True)),
                ('category', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('features', models.TextField(blank=True, null=True)),
                ('miscellaneous', models.CharField(blank=True, max_length=3000, null=True)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LikeButton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ManyToManyField(blank=True, related_name='likebutton', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=3000, null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('approved_comment', models.BooleanField(default=False)),
                ('number_of_comments', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Comments',
                'ordering': ['last_update'],
            },
        ),
    ]
