
import json
#import requests
from django.contrib import messages
from django.contrib.auth import models
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from test_files import ebay_products, amazon_products
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from .models import Product, Comments, LikeButton
from .forms import CommentForm, AddProductForm, EditCommentForm
from django.views.generic import UpdateView

debug_gp = True
amazon_responses = amazon_products.amazon_responses
ebay_responses = ebay_products.ebay_responses



# List of products

def products(request):
    
    context ={'products': Product.objects.all()[:10]
    }
    
    return render(request, "products.html", context)

# Specific product detail

def product_detail(request, pk):
    template_name = 'products/product_detail.html'  
    products = Product.objects.get(pk=pk)  
    if request.method == 'POST':
        print("step 1")
        form = CommentForm(request.POST or None)
        if form.is_valid():
            print("step 2")
            content = request.POST.get('content')
            comment = Comments.objects.create(products = products, user = request.user, content = content)
            comment.save()
            return HttpResponseRedirect (template_name)
    else:
        form = CommentForm()
        print("step 2")
        
    return render(request, template_name, {'form':form} )


def add_comment(request, pk):
    template_name = 'products/product_detail.html'

    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
       
        user=request.user
        content=request.POST.get('comment_body')
        comments=Comments(user=user, content=content, product=product)
        comments.save()
        
        return redirect('products/product_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, template_name, {'form': form, 'pk':pk})



@login_required
def edit_comments(request, id):
    context = {}
    products = get_object_or_404(Product)
    # comments = Comments.objects.get(id)
    comments = get_object_or_404(Comments, 'content')
    content=request.POST.get('comment_body')
    editform = EditCommentForm(request.POST, instance=comments)
    comments.save(id=id)    
    context = {'products':products, 'editform':editform, 'comments':comments, 'content':content}
        
        # return redirect(aargs={"id":id}, kwargs={"pk": products.pk}) 
        # return HttpResponseRedirect(products/product_detail)
     

    return render(request, 'edit_comments.html', )

# Delete comment
@login_required
def deletecomment(request, comments_id):
    context = {}
    products = get_object_or_404(Product, id=id)
    # comments = Comments.objects.get(id)
    comments = get_object_or_404(Comments, id=comments_id)
    form = CommentForm()
    comments.delete()
    context = {'comments':comments, 'comments_id':comments_id}
    return render(request, 'deletecomment.html', )


# Edit Comment


# Show list of products
class ProductListView(generic.ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.order_by('product_name')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductListView, self).get_context_data(**kwargs)
        # For displaying rows
        products = self.object_list
        count = products.count()
        iterations = int(count / 5)
        if count % 5 > 0:
            iterations += 1
        slices = []
        for i in range(iterations):
            slices.append(f"{i * 5}:{5 * (i + 1)}")
        context['slices'] = slices
        return context




# Like button
def like_button(request):
    if request.method == "POST":
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            likes_id = request.POST.get("likes_id", None)
            like_object = get_object_or_404(LikeButton, pk=likes_id)

            # Check if user already liked product
            if like_object.user.filter(id=request.user.id):
                # Remove user like from product
                like_object.user.remove(request.user)
                liked = False
            else:
                # Add user like to product
                like_object.user.add(request.user)
                liked = True

            # Create new context to feed back to AJAX call
            context = {"likes_count": like_object.total_likes,
                       "user_like"  : liked,
                       "likes_id"   : likes_id
                       }
            return HttpResponse(json.dumps(context), content_type='application/json')


def add_product_view(request):
    # Check if request was POST
    if request.method == 'POST':
        # Get amazon_asin & ebay_url
        amazon_asin = request.POST.get('amazon_asin')
        ebay_url = request.POST.get('ebay_url')

        # Get respective data
        amazon_product = get_amazon_product(amazon_asin)
        ebay_product = get_ebay_product(ebay_url)

        # Get or create product
        product, created = get_create_product(amazon_product, ebay_product)

        if product:
            if not created:
                messages.success(request, f"\"{product.product_name}\" has been updated")
            else:
                messages.success(request, f"\"{product.product_name}\" has been created")
        else:
            messages.error(request, f"Error: {created}")

    # Render page with any bound data and error messages
    context = {'form': AddProductForm()}
    return render(request, 'products/add_product.html', context)


def delete_product(request, product_id):
    redirect_url = request.META["HTTP_REFERER"]
    # Retrieve product
    product = get_object_or_404(Product, pk=product_id)
    # Delete product
    product.delete()
    return redirect(redirect_url)


# Get amazon product from asin
def get_amazon_product(amazon_asin):
    url = "https://amazon-products1.p.rapidapi.com/product"
    querystring = {"country": "US", "asin": amazon_asin}
    headers = {
        'x-rapidapi-key' : 'cd09594deamshbb8b2478ed8a011p1e756ajsnc0216f4bdfad',
        'x-rapidapi-host': 'amazon-products1.p.rapidapi.com'
        }

    if debug_gp:
        response = amazon_responses[int(amazon_asin)]
    else:
        response = requests.request("GET", url, headers=headers, params=querystring).json()

    amazon_context = {
        'asin'       : response['asin'],
        'price'      : response['prices']['current_price'],
        'description': response['description'],
        'features'   : response['features'],
        'image_urls' : response['images'],
        'url'        : response['full_link']
        }
    return amazon_context


# Get ebay product from url
def get_ebay_product(ebay_url):
    url = "https://ebay-com.p.rapidapi.com/product"
    querystring = {
        "URL": ebay_url
        }
    headers = {
        'x-rapidapi-key' : "cd09594deamshbb8b2478ed8a011p1e756ajsnc0216f4bdfad",
        'x-rapidapi-host': "ebay-products.p.rapidapi.com"
        }

    if debug_gp:
        response = ebay_responses[int(ebay_url)]
    else:
        response = requests.request("GET", url, headers=headers, params=querystring).json()

    ebay_context = {
        'name'      : response['title'],
        'price'     : response['prices']['current_price'],
        'url'       : response['full_link'],
        'image_urls': response['images'],
        'category'  : response['category'],
        }
    return ebay_context


# Get or crete product
def get_create_product(amazon_product, ebay_product):
    # Try to find a valid image url
    image_url = staticfiles_storage.url("/images/product_images/image_not_found.png")
    for image in amazon_product['image_urls'] + ebay_product['image_urls']:
        if image:
            image_url = image
            break

    # Create a product
    try:
        product, created = Product.objects.update_or_create(
                amazon_asin=amazon_product['asin'],
                defaults={'product_name': ebay_product['name'],
                          'description' : amazon_product['description'],
                          'amazon_price': amazon_product['price'],
                          'ebay_price'  : ebay_product['price'],
                          'amazon_url'  : amazon_product['url'],
                          'ebay_url'    : ebay_product['url'],
                          'category'    : ebay_product['category'],
                          'features'    : amazon_product['features'],
                          'image'       : image_url,
                          }
                )

        # Save product (to generate product pk)
        product.save()

        # Return product, created
        return product, created
    except ValidationError as e:
        return False, e
    except LookupError as e:
        return False, e

