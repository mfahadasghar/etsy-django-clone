from .models import CartItem, WishlistItem

def cart_and_wishlist_counts(request):
    if request.user.is_authenticated and request.user.is_buyer:
        cart_count = CartItem.objects.filter(user=request.user).count()
        wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0
        wishlist_count = 0

    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    }