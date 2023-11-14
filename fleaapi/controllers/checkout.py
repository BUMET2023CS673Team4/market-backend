import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST

from fleaapi.provider.secret_provider import SecretProvider


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
def create_checkout_session(request):
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
    stripe.api_key = SecretProvider().get_secret('stripe', 'test_secret_key')
    try:
        product = stripe.Product.create(
            name='Test product',
            description='Test product description',
        )
        price = stripe.Price.create(
            product=product.stripe_id,
            unit_amount=1000,
            currency='usd',
        )
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
            return_url=request.build_absolute_uri('/return.html?stripe_sid=')
            + '{CHECKOUT_SESSION_ID}',
        )
        return JsonResponse({'client_secret': session.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
