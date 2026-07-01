from django.urls import path
from .views import trade_list, trade_detail, trade_image_create, trade_image_delete

urlpatterns = [
    path('api/v2/trades/', trade_list, name='trade-list'),
    path('api/v2/trades/<int:pk>/', trade_detail, name='trade-detail'),
    path('api/v2/trades/<int:trade_id>/images/', trade_image_create, name='trade-image-create'),
    path('api/v2/trades/<int:trade_id>/images/<int:image_id>/', trade_image_delete, name='trade-image-delete'),
]