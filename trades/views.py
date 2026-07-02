import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Trade, TradeImage
from .utils import serialize_trade_list, serialize_trade_detail
from .decorators import api_login_required, require_auth_for_methods

User = get_user_model()

@csrf_exempt
@require_http_methods(["GET", "POST"])
@require_auth_for_methods(['POST'])
def trade_list(request):
    if request.method == "GET":
        trades = Trade.objects.filter(status='open')
        data = [serialize_trade_list(t) for t in trades]
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid JSON'}, status=400)

        title = body.get('title', '').strip()
        description = body.get('description', '').strip()
        status = body.get('status', 'open')

        errors = {}
        if not title:
            errors['title'] = ['This field is required.']
        if not description:
            errors['description'] = ['This field is required.']
        if status not in ('open', 'closed'):
            errors['status'] = ['Must be "open" or "closed".']

        if errors:
            return JsonResponse(errors, status=400)

        trade = Trade.objects.create(
            author=request.user,
            title=title,
            description=description,
            status=status
        )
        return JsonResponse(serialize_trade_detail(trade, request), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT"])
@require_auth_for_methods(['PUT'])
def trade_detail(request, pk):
    trade = get_object_or_404(Trade, pk=pk)

    if request.method == "GET":
        return JsonResponse(serialize_trade_detail(trade, request))

    elif request.method == "PUT":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid JSON'}, status=400)

        title = body.get('title')
        description = body.get('description')
        status = body.get('status')

        errors = {}
        if title is not None and not title.strip():
            errors['title'] = ['This field cannot be blank.']
        if description is not None and not description.strip():
            errors['description'] = ['This field cannot be blank.']
        if status is not None and status not in ('open', 'closed'):
            errors['status'] = ['Must be "open" or "closed".']

        if errors:
            return JsonResponse(errors, status=400)

        if title is not None:
            trade.title = title.strip()
        if description is not None:
            trade.description = description.strip()
        if status is not None:
            trade.status = status

        trade.save()
        return JsonResponse(serialize_trade_detail(trade, request))


@csrf_exempt
@require_http_methods(["POST"])
@api_login_required
def trade_image_create(request, trade_id):
    trade = get_object_or_404(Trade, pk=trade_id)

    if 'image' not in request.FILES:
        return JsonResponse({'image': ['No image file provided.']}, status=400)

    image_file = request.FILES['image']
    image = TradeImage.objects.create(
        author=request.user,
        trade=trade,
        image=image_file
    )

    data = {
        'id': image.id,
        'image': request.build_absolute_uri(image.image.url),
        'created_at': image.created_at.isoformat(),
        'updated_at': image.updated_at.isoformat(),
        'delete_url': request.build_absolute_uri(
            f'/api/v2/trades/{trade.id}/images/{image.id}/'
        )
    }
    return JsonResponse(data, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
@api_login_required
def trade_image_delete(request, trade_id, image_id):
    image = get_object_or_404(TradeImage, pk=image_id, trade_id=trade_id)
    image.delete()
    return JsonResponse({}, status=204)