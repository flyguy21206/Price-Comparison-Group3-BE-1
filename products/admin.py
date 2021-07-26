
from django.contrib import admin
from .models import Product, Comments

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['product_name', 'pk', 'image', 'amazon_price','ebay_price', 'description', 'miscellaneous','created_at', 'updated_at']
    list_filter = ['product_name', 'amazon_price','ebay_price', 'updated_at', 'description']
    search_fields = ['product_name', 'amazon_price','ebay_price', 'description', 'miscellaneous','created_at', 'updated_at']

class CommentAdmin(admin.ModelAdmin):
    model = Comments
    list_display = ('product','content', 'last_update', 'user', 'id', 'pk')
    list_filter = ['product', 'last_update']
    search_fields = ['product','content', 'last_update', 'user']
    


admin.site.register(Product, ProductAdmin)
admin.site.register(Comments, CommentAdmin)



