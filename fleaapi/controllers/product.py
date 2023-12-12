# product page
# 1 get product by id

import json
import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from django.views.decorators.http import require_GET

from fleaapi.models import Cart, Category, Item, User


@require_GET
def get_product_by_id(request: HttpRequest, product_id) -> HttpResponse:
    """
    Get product by id.

    Endpoint: GET /api/products/<int:product_id>/
    GET Parameters:
        product_id: the id of the product
    :param request: the request object
    :param product_id: the id of the product
    :return: HttpResponse
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


def add_item_to_cart(request: HttpRequest, product_id) -> HttpResponse:
    """
    Add item to cart, requires user_id in session.

    Endpoint: POST /api/products/<int:product_id>/add-to-cart/
    POST parameters:
        None
    Session requirements:
        user_id: the id of the user (obtained via login)
    :param request: HttpRequest
    :param product_id: the id of the product
    :return: HttpResponse
    """
    logger = logging.getLogger(__name__)
    logger.info("[add_item_to_cart] flow started")
    user_id = request.session.get("user_id")
    if not user_id or not product_id:
        logger.error(f"[add_item_to_cart] missing user_id or product_id")
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
