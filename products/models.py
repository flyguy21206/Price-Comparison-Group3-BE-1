# Framework for Price Comparison tool

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

User = get_user_model()


class Product(models.Model):
    product_name = models.CharField(max_length=512, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    amazon_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ebay_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amazon_url = models.URLField(blank=True, null=True, default=None)
    ebay_url = models.URLField(blank=True, null=True, default=None)
    amazon_asin = models.CharField(max_length=12, blank=True, null=True, default=None)
    category = models.CharField(max_length=200, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    miscellaneous = models.CharField(max_length=3000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    
    @property
    def count_likes(self):
        return self.liked.filter().count()

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("products/product_detail", kwargs={"id":self.id})

class Comments(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    content = models.TextField(max_length=3000, blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    
    def get_absolute_url(self):
        return reverse("products/product_detail", kwargs={"id":self.id})


    class Meta:
        verbose_name_plural = "Comments"
        ordering = ['last_update']
  
    def __str__(self):
        return 'Comment on {} by {}'.format(self.content, self.user)
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"id":self.id})
        # return "/product_details/%s/"%(self.id)

LIKE_CHOICES = {
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
}

class LikeButton(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, related_name='productlikes')
    user = models.ForeignKey(User, blank=True, related_name='likebutton', null=True, on_delete=models.CASCADE)
    product_like = models.CharField(choices=LIKE_CHOICES, default="Like", max_length=7)
 
    def total_likes(self):
        return (self.product, self.product_like)

