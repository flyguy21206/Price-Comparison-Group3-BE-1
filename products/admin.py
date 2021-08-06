
from django.contrib import admin
from .models import Product, Comments, LikeButton

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['product_name', 'count_likes', 'pk', 'image', 'amazon_price','ebay_price', 'description', 'miscellaneous','created_at', 'updated_at', 'amazon_url', 'ebay_url']
    list_filter = ['product_name', 'amazon_price','ebay_price', 'updated_at', 'description']
    search_fields = ['product_name', 'amazon_price','ebay_price', 'description', 'miscellaneous','created_at', 'updated_at']

class CommentAdmin(admin.ModelAdmin):
    model = Comments
    list_display = ('product','content', 'last_update', 'user', 'id')
    list_filter = ['product', 'last_update']
    search_fields = ['product','content', 'last_update', 'user']

class LikeButtonAdmin(admin.ModelAdmin):
    model = LikeButton
    list_display = ('product_like', 'user', 'product', 'id') 


admin.site.register(Product, ProductAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(LikeButton, LikeButtonAdmin)
