from django.http import JsonResponse
# from .models import Item
from fleaapi.models import Item

# get homepage items API
def get_homepage_items(request):
    items = list(Item.objects.values())
    return JsonResponse({'items': items})

# get category items API
def get_category_items(request):
    category_id = request.GET.get('category', None)
    if category_id is not None:
        items = list(Item.objects.filter(category_id=category_id).values())
    else:
        items = []
    return JsonResponse({'items': items})

# search items API
def search_items(request):
    query = request.GET.get('search', '')
    items = list(Item.objects.filter(name__icontains=query).values())
    return JsonResponse({'items': items})


# get item details API
def get_item_details(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        response_data = {
            'name': item.name,
            'price': item.price,
            'description': item.description,
            # 其他字段
        }
        return JsonResponse({'status': 'success', 'item': response_data})
    except Item.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Item not found'})


# 添加商品到购物车
def add_to_cart(request):
    item_id = request.POST.get('item_id')
    quantity = request.POST.get('quantity')
    # user must be authenticated then could add item to cart
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, item_id=item_id)
        cart.quantity = quantity
        cart.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'message': 'User not authenticated'})

# remove item from cart API
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, item_id=item_id)
            cart.delete()
            return JsonResponse({'status': 'success'})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Item not in cart'})
    else:
        return JsonResponse({'status': 'failed', 'message': 'User not authenticated'})
