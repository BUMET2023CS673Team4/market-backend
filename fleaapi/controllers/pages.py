from django.db.models import Min
from django.http import JsonResponse

from fleaapi.models import Category, Item


def all_categories(request):
    """
    This function returns all categories as a JSON response, used to fill the content in the header.
    Endpoint: GET /api/categories/

    GET parameters:
        None
    :param request: the request object
    :return: the json response with all categories
    """
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


def homepage(request):
    """
    This function returns the homepage data as a JSON response.

    The json array consists of the top 3 categories and the url to the images of the first item in each category.

    Endpoint: GET /api/homepage/

    GET parameters:
        None
    :param request: the request object
    :return: the json response with the homepage data
    """
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
                "image": item.image,
            }
            for category in top_categories
            for item in items
            if item.category_id == category
        ],
        safe=False,
    )
