import json
import logging

import stripe
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST

from fleaapi.provider.secret_provider import SecretProvider

from .cart import show_items_in_cart


@csrf_protect
@require_GET
def stripe_public_key(request):
    """
    Get the stripe public key.
    This API is required by the stripe process.
    No parameters are required for now.
    Endpoint: GET /api/stripe-public-key/
    Get parameters:
        None
    :param request: the request object
    :return: the json response with the stripe public key
    """
    stripe_public_key = SecretProvider().get_secret('stripe', 'test_public_key')
    return JsonResponse({'public_key': stripe_public_key})


@require_POST
def create_checkout_session(request: HttpRequest) -> HttpResponse:
    """
    Create a checkout session and return the client secret to the frontend.
    This API is required by the stripe process.
    No parameters are required for now.
    Endpoint: POST /api/create-checkout-session/
    Post Form Data:
        None
    :param request: the request object
    :return: the json response with the client secret
    """
    logger = logging.getLogger(__name__)
    logger.info("[create_checkout_session] flow started")
    try:
        items_in_cart = show_items_in_cart(request)
        if items_in_cart.status_code != 200:
            logger.error(f"[create_checkout_session] show_items_in_cart failed")
            return HttpResponseBadRequest()
        items_total_price = json.loads(items_in_cart.content)['total_price']
        if items_total_price < 1:
            logger.error(f"[create_checkout_session] total price is less than 1 cent")
            return HttpResponseBadRequest()
    except Exception as e:
        logger.error(f"[create_checkout_session] failed: {repr(e)}")
        return JsonResponse({'error': str(e)}, status=500)

    stripe.api_key = SecretProvider().get_secret('stripe', 'test_secret_key')
    logger.info("[create_checkout_session] stripe api key set")
    try:
        product = stripe.Product.create(
            name='Test product',
            description='Test product description',
        )
        logger.info(f"[create_checkout_session] product created")
        price = stripe.Price.create(
            product=product.stripe_id,
            unit_amount=int(items_total_price * 100),
            currency='usd',
        )
        logger.info(f"[create_checkout_session] price created: {price.unit_amount}")
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_id,
                    'quantity': 1,
                }
            ],
            mode='payment',
            redirect_on_completion='never',
        )
        logger.info(f"[create_checkout_session] session created: {session.id}")
        return JsonResponse({'client_secret': session.client_secret})
    except Exception as e:
        logger.error(f"[create_checkout_session] failed: {repr(e)}")
        return JsonResponse({'error': repr(e)}, status=500)


@csrf_protect
@require_GET
def session_status(request):
    """
    Get the status of the checkout session.
    This API is optional to the stripe checkout process.
    Endpoint: GET /api/session-status/
    Get parameters:
        stripe_sid: The stripe session id.
    :param request: the request object
    :return: the json response with the status of the checkout session
    """
    stripe.api_key = SecretProvider().get_secret('stripe', 'test_secret_key')
    try:
        session = stripe.checkout.Session.retrieve(request.GET['stripe_sid'])
        return JsonResponse(
            {'status': session.status, 'customer_email': session.customer_details.email}
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
