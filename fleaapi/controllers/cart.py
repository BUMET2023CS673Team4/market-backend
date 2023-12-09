from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.http import require_GET
from django.db.models import Q
import logging
from fleaapi.models import Item, Category
from fleaapi.models import User
from fleaapi.models import Cart
from fleaapi.models import User
import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
import logging
from fleaapi.models import Cart

# return all items in cart
# return amoount of items in cart
# return total price of items in cart
@require_GET
def show_items_in_cart(request):
    logger = logging.getLogger(__name__)
    logger.info("[show_items_in_cart] flow started")
    user_id = request.GET.get("user_id")
    if not user_id:
        logger.error(f"[show_items_in_cart] missing required fields")
        return HttpResponseBadRequest()
    try:
        # there could be multiple items in carts
        # get all items in cart
        cart = Cart.objects.filter(user_id=user_id)
        
        items_info = []
        for cart_item in cart:
            item_id = cart_item.item_id  # 假设 Cart 模型中有一个指向 Item 的 ForeignKey 名为 item
            items_info.append(model_to_dict(item_id))
        # 
        amount = len(items_info)
        total_price = 0
        for item in items_info:
            total_price += item['price']


        logger.info(f"[show_items_in_cart] show items in cart: {user_id}")
        return JsonResponse({"cart": items_info,"amount":amount,"total_price":total_price}, safe=False)
    
    except Exception as e:
        logger.error(
            f"[show_items_in_cart] show items in cart {user_id} failed: {repr(e)}"
        )
        return HttpResponseServerError()