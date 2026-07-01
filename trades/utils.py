def serialize_trade_list(trade):
    return {
        'id': trade.id,
        'title': trade.title,
        'created_at': trade.created_at.isoformat()
    }

def serialize_trade_detail(trade, request):
    images = trade.images.all()
    return {
        'id': trade.id,
        'title': trade.title,
        'description': trade.description,
        'status': trade.status,
        'created_at': trade.created_at.isoformat(),
        'updated_at': trade.updated_at.isoformat(),
        'author': {
            'id': trade.author.id,
            'username': trade.author.username,
            'email': trade.author.email,
            'phone': trade.author.phone
        },
        'images': [
            {
                'id': img.id,
                'image': request.build_absolute_uri(img.image.url),
                'created_at': img.created_at.isoformat(),
                'updated_at': img.updated_at.isoformat(),
                'delete_url': request.build_absolute_uri(
                    f'/api/v2/trades/{trade.id}/images/{img.id}/'
                )
            } for img in images
        ],
        'images_url': request.build_absolute_uri(
            f'/api/v2/trades/{trade.id}/images/'
        )
    }