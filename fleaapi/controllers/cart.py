import logging

from django.forms.models import model_to_dict
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse,
)
from django.views.decorators.http import require_GET

from fleaapi.models import Cart, Category, Item, SellerProfile, User


def show_items_in_cart(request: HttpRequest) -> HttpResponse:
    """
    Show items in cart, requires user_id in session.
    Endpoint: GET /api/show-items-in-cart/
    GET parameters:
        None
    Session requirements:
        user_id: the id of the user (obtained via login)
    :param request: HttpRequest
    :return: HttpResponse
    """
    logger = logging.getLogger(__name__)
    logger.info("[show_items_in_cart] flow started")
    user_id = request.session.get("user_id")
    if not user_id:
        logger.error(f"[show_items_in_cart] user not logged in")
        return HttpResponseBadRequest()
    try:
        # there could be multiple items in carts
        # get all items in cart
        cart = Cart.objects.filter(user_id=user_id)

        items_info = []
        item_id_set = set()
        for cart_item in cart:
            item_id = cart_item.item_id  # 假设 Cart 模型中有一个指向 Item 的 ForeignKey 名为 item
            if item_id not in item_id_set:
                items_info.append(model_to_dict(item_id))
                item_id_set.add(item_id)

        for i in items_info:
            seller_profile = SellerProfile.objects.get(id=i['seller_id'])
            seller_user_name = seller_profile.user.name
            i['seller_user_name'] = seller_user_name

        amount = len(items_info)
        total_price = 0
        for item in items_info:
            total_price += item['price']

        logger.info(f"[show_items_in_cart] show items in cart: {user_id}")
        return JsonResponse(
            {"cart": items_info, "amount": amount, "total_price": total_price},
            safe=False,
        )

    except Exception as e:
        logger.error(
            f"[show_items_in_cart] show items in cart {user_id} failed: {repr(e)}"
        )
        return HttpResponseServerError()
