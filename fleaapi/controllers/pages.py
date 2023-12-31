import logging

from django.db.models import Min
from django.http import HttpRequest, HttpResponse, JsonResponse

from fleaapi.models import Category, Item


def all_categories(request: HttpRequest) -> HttpResponse:
    """
    This function returns all categories as a JSON response, used to fill the content in the header.
    Endpoint: GET /api/categories/

    GET parameters:
        None
    :param request: the request object
    :return: the json response with all categories
    """
    logger = logging.getLogger(__name__)
    logger.info("[all_categories] called")
    # return all categories as a json response
    return JsonResponse(
        {
            "categories": [
                {
                    "id": category.id,
                    "name": category.name,
                }
                for category in Category.objects.all()
            ]
        }
    )


def homepage(request: HttpRequest) -> HttpResponse:
    """
    This function returns the homepage data as a JSON response.

    The json array consists of the top 3 categories and the url to the images of the first item in each category.

    Endpoint: GET /api/homepage/

    GET parameters:
        None
    :param request: the request object
    :return: the json response with the homepage data
    """
    logger = logging.getLogger(__name__)
    logger.info("[homepage] called")
    TOP_CATEGORY_COUNT = 3
    top_categories = Category.objects.all()[:TOP_CATEGORY_COUNT]

    min_ids_items = (
        Item.objects.filter(category_id__in=top_categories)
        .values("category_id")
        .annotate(min_id=Min("id"))
    )

    items = Item.objects.filter(id__in=[item["min_id"] for item in min_ids_items])
    return JsonResponse(
        [
            {
                "id": category.id,
                "name": category.name,
                "media_image": item.image,
            }
            for category in top_categories
            for item in items
            if item.category_id == category
        ],
        safe=False,
    )


def category_items(request: HttpRequest, category_id) -> HttpResponse:
    """
    This function returns the items in a category as a JSON response.

    Endpoint: GET /api/categories/<int:category_id>/items/?page=<int:page>

    GET parameters:
        category_id: the id of the category
    :param request: the request object
    :return: the json response with the items in the category
    """
    # return the items in the category as a json response
    logger = logging.getLogger(__name__)
    logger.info(f"[category_items] called with category_id={category_id}")
    ITEMS_PER_PAGE = 10
    try:
        page = int(request.GET.get("page", 1))
        if page <= 0:
            page = 1
    except ValueError:
        page = 1
    logger.info(f"[category_items] sanitized_page={page}")
    start = (page - 1) * ITEMS_PER_PAGE
    end = page * ITEMS_PER_PAGE
    items = Item.objects.filter(category_id=category_id)[start:end]
    return JsonResponse(
        {
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price,
                    "media_image": item.image,
                }
                for item in items
            ]
        }
    )
