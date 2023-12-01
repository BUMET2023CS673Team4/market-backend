from django.views.decorators.http import require_POST

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)

from fleaapi.models import Item

@require_POST
def get_product(request: HttpRequest) -> HttpResponse :
    search_name = request.POST.get("name")
    #search for the item
    if not name :
        return HttpResponseBadRequest('Neea parameter called name!')
    try:
        result_items = Item.objects.filter(name=search_name)
        serialized_data = serialize('json', result_items)
        return JsonResponse({'items': serialized_data}, safe=False)
    
    except Item.DoesNotExist:
        return JsonResponse({'error': f'Item with name {item_name} not found'}, status=404)