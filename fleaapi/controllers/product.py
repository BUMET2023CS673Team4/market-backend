# product page
# 1 get product by id

import json
import logging

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.http import require_GET

from fleaapi.models import Cart, Category, Item, User


@require_GET
def get_product_by_id(request, product_id):
    """
    Get product by id.

    Endpoint: GET /api/products/<int:product_id>/
    GET Parameters:
        product_id: the id of the product
    :param request: the request object
    :param product_id: the id of the product
    """
    logger = logging.getLogger(__name__)
    logger.info("[get_product_by_id] flow started")
    if not product_id:
        logger.error(f"[get_product_by_id] missing required fields")
        return HttpResponseBadRequest()
    try:
        product = Item.objects.get(id=product_id)
        logger.info(f"[get_product_by_id] get product by id: {product_id}")
        return HttpResponse(
            json.dumps(model_to_dict(product), cls=DjangoJSONEncoder),
            content_type="application/json",
        )
    except Exception as e:
        logger.error(
            f"[get_product_by_id] get product by id {product_id} failed: {repr(e)}"
        )
        return HttpResponseServerError()


# 2 add item to user's cart
@require_GET
def add_item_to_cart(request):
    logger = logging.getLogger(__name__)
    logger.info("[add_item_to_cart] flow started")
    user_id = request.GET.get("user_id")
    product_id = request.GET.get("product_id")
    if not user_id or not product_id:
        logger.error(f"[add_item_to_cart] missing required fields")
        return HttpResponseBadRequest()
    try:
        user = User.objects.get(id=user_id)
        product = Item.objects.get(id=product_id)
        cart = Cart.objects.create(user_id=user, item_id=product)
        cart.full_clean()
        cart.save()
        logger.info(f"[add_item_to_cart] add item to cart: {product_id}")
        return HttpResponse(status=201)
    except Exception as e:
        logger.error(
            f"[add_item_to_cart] add item to cart {product_id} failed: {repr(e)}"
        )
        return HttpResponseServerError()
