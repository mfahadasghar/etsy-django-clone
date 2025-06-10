from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import *
from .models import *  
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
import random
from django.db.models import *

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    
    ) if query else []
    return render(request, 'search_results.html', {
        'query': query,
        'products': products
    })
    
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect('landing')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landing')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

from django.shortcuts import render, redirect
from main.models import Product, Shop
from django.db.models import Count
import random

from django.shortcuts import render, redirect
from .models import Shop, Product
from django.db.models import Count
import random

def landing_view(request):
    # Redirect seller to their dashboard
    if request.user.is_authenticated and request.user.is_seller:
        return redirect('seller_dashboard')

    # Get the current user's shop (if any)
    user_shop = None
    if request.user.is_authenticated:
        user_shop = Shop.objects.filter(owner=request.user).first()

    # Exclude products from the user's own shop
    if user_shop:
        products = Product.objects.exclude(shop=user_shop)
    else:
        products = Product.objects.all()

    # Fetch 16 popular products
    popular_products = products.annotate(order_count=Count('order_items')).order_by('-order_count')[:16]

    # Fetch 16 newest products (recently added)
    inspired_products = products.order_by('-created_at')[:16]

    # Fetch 16 random products
    product_list = list(products)
    random_products = random.sample(product_list, min(len(product_list), 16))

    return render(request, 'landing.html', {
        'random_products': random_products,
        'inspired_products': inspired_products,  # ✅ valid context key
        'popular_products': popular_products,
    })

  
@login_required
def my_shop_view(request):
    try:
        shop = Shop.objects.get(owner=request.user)
        return redirect('shop_detail', shop_id=shop.id)
    except Shop.DoesNotExist:
        return redirect('create_shop')

@login_required
def create_shop(request):
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            return redirect('shop_detail', shop_id=shop.id)
    else:
        form = ShopForm()
    return render(request, 'shop_form.html', {'form': form, 'edit': False})


@login_required
def edit_shop(request):
    shop = get_object_or_404(Shop, owner=request.user)
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shop_detail', shop_id=shop.id)
    else:
        form = ShopForm(instance=shop)
    return render(request, 'shop_form.html', {'form': form, 'edit': True})

def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    products = Product.objects.filter(shop=shop)
    return render(request, 'shop_detail.html', {'shop': shop, 'products': products})


















@login_required
def add_product(request):
    try:
        shop = Shop.objects.get(owner=request.user)
    except Shop.DoesNotExist:
        return redirect('my_shop')  # redirect to create shop first

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()
            return redirect('shop_detail', shop_id=shop.id)
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.shop.owner != request.user:
        return HttpResponseForbidden("You do not have permission to edit this product.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop_detail', shop_id=product.shop.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_form.html', {'form': form, 'edit': True})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.shop.owner != request.user:
        return HttpResponseForbidden("You do not have permission to delete this product.")

    if request.method == 'POST':
        shop_id = product.shop.id
        product.delete()
        return redirect('shop_detail', shop_id=shop_id)

    return render(request, 'product_confirm_delete.html', {'product': product})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id) if product.category else []
    shop_products = Product.objects.filter(shop=product.shop).exclude(id=product.id)

    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
        'shop_products': shop_products
    })

@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    if request.user.is_buyer:
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    return redirect('view_cart')





   




@login_required
def add_to_wishlist(request, product_id):
    if request.user.is_buyer:
        product = get_object_or_404(Product, id=product_id)
        WishlistItem.objects.get_or_create(user=request.user, product=product)
        
    return redirect('view_wishlist')


@login_required
def view_wishlist(request):
    items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})


@require_POST
@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('view_cart')

@require_POST
@login_required
def remove_from_wishlist(request, item_id):
    WishlistItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('view_wishlist')

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })
    
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('view_cart')

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Simulate payment success
        order = Order.objects.create(buyer=request.user, total_price=total, is_paid=True)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            # Optionally reduce stock
            item.product.stock >= item.quantity
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()  # clear cart after order placed
        return render(request, 'checkout_success.html', {'order': order})

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })
    
@login_required
def view_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def seller_orders(request):
    if not request.user.is_seller:
        return redirect('home')

    order_items = OrderItem.objects.filter(product__shop__owner=request.user).order_by('-order__created_at')
    return render(request, 'seller_orders.html', {'order_items': order_items})



@require_POST
@login_required
def update_order_status(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, product__shop__owner=request.user)
    new_status = request.POST.get('status')

    if new_status in dict(OrderItem.STATUS_CHOICES):
        item.status = new_status
        item.save()

    return redirect('seller_orders')


@login_required
def leave_review(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__buyer=request.user)

    if order_item.status != 'delivered' or hasattr(order_item, 'review'):
        return redirect('view_orders')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = order_item.product
            review.buyer = request.user
            review.order_item = order_item
            review.save()
            return redirect('view_orders')
    else:
        form = ReviewForm()

    return render(request, 'leave_review.html', {'form': form, 'product': order_item.product})

@login_required
def chat_with_seller(request, seller_id):
    seller = get_object_or_404(User, id=seller_id)
    if seller == request.user:
        return redirect('home')

    thread, created = MessageThread.objects.get_or_create(buyer=request.user, seller=seller)

    return redirect('view_thread', thread_id=thread.id)

@login_required
def view_thread(request, thread_id):
    thread = get_object_or_404(MessageThread, id=thread_id)
    if request.user != thread.buyer and request.user != thread.seller:
        return redirect('home')

    messages = thread.messages.order_by('sent_at')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.thread = thread
            msg.sender = request.user
            msg.save()
            return redirect('view_thread', thread_id=thread.id)
    else:
        form = MessageForm()

    return render(request, 'chat/thread.html', {
        'thread': thread,
        'messages': messages,
        'form': form
    })
    
@login_required
def inbox(request):
    if request.user.is_seller:
        threads = MessageThread.objects.filter(seller=request.user)
    else:
        threads = MessageThread.objects.filter(buyer=request.user)
    
    return render(request, 'chat/inbox.html', {'threads': threads})


@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        return redirect('home')

    # Get seller’s products 
    seller_products = Product.objects.filter(shop__owner=request.user)

    # Order items that belong to this seller’s products
    order_items = OrderItem.objects.filter(product__in=seller_products)

    total_sales = order_items.aggregate(total=Sum('price'))['total'] or 0
    total_orders = order_items.values('order').distinct().count()
    total_products_sold = order_items.aggregate(qty=Sum('quantity'))['qty'] or 0

    return render(request, 'dashboard/seller_dashboard.html', {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_products_sold': total_products_sold,
        'order_items': order_items
    })
    
    
    
def about_us(request):
    return render(request, 'about_us.html')

def team_view(request):
    return render(request, 'team_view.html')

def about_detail(request):
    return render(request, 'about_detail.html')

def impact_view(request):
    return render(request, 'impact_view.html')








def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')































