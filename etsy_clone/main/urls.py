from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', landing_view, name='landing'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('shop/<int:shop_id>/', shop_detail, name='shop_detail'),
    path('my-shop/add-product/', add_product, name='add_product'),
    path('my-shop/', my_shop_view, name='my_shop'),
    path('my-shop/create/', create_shop, name='create_shop'),
    path('my-shop/edit/', edit_shop, name='edit_shop'),
    path('product/<int:product_id>/edit/', edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', delete_product, name='delete_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', view_wishlist, name='view_wishlist'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('category/<slug:slug>/', category_products, name='category_products'),
    path('search/', search_products, name='search_products'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', view_orders, name='view_orders'),
    path('seller/orders/', seller_orders, name='seller_orders'),
    path('seller/orders/update/<int:item_id>/', update_order_status, name='update_order_status'),
    path('review/<int:item_id>/', leave_review, name='leave_review'),
    path('chat/start/<int:seller_id>/', chat_with_seller, name='chat_with_seller'),
    path('chat/<int:thread_id>/', view_thread, name='view_thread'),
    path('chat/', inbox, name='inbox'),
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('about-us/', about_us, name='about_us'),
    path('about-us/team/', team_view, name='team_view'),
    path('about-us/detail/', about_detail, name='about_detail'),
    path('about-us/impact/', impact_view, name='impact_view'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
]


























