from django.urls import path
from . import views


app_name = 'products'
urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    
    path('deletecomment/<int:id>', views.deletecomment, name="deletecomment"),
    # path('<int:pk>/add_comment/', views.add_comment, name="add_comment"),

    path('edit_comments/<int:id>', views.edit_comments, name="edit_comments"),
   
    



    # Likes
    path('like/', views.like_button, name='like'),

    # Add and Delete Product
    path('add_products/', views.add_product_view, name='add_products'),
    path('delete_product/<int:product_id>', views.delete_product, name='delete_product'),
    ]

