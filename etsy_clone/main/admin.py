from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Shop)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Order)  
admin.site.register(Message)
admin.site.register(MessageThread)
admin.site.register(OrderItem)
admin.site.register(Product)