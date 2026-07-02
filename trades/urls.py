from django.urls import path
from .views import (
    trade_list,
    trade_detail,
    trade_image_create,
    trade_image_delete
)
from .views_drf import (
    TradeListCreateView,
    TradeRetrieveUpdateView,
    TradeImageCreateView,
    TradeImageDestroyView
)

urlpatterns = [
    # Чистый Django (старая версия)
    path('api/v2/trades/', trade_list, name='trade-list'),
    path('api/v2/trades/<int:pk>/', trade_detail, name='trade-detail'),
    path('api/v2/trades/<int:trade_id>/images/', trade_image_create, name='trade-image-create'),
    path('api/v2/trades/<int:trade_id>/images/<int:image_id>/', trade_image_delete, name='trade-image-delete'),

    # DRF v2
    path('api/v2/drf/trades/', TradeListCreateView.as_view(), name='drf-trade-list'),
    path('api/v2/drf/trades/<int:pk>/', TradeRetrieveUpdateView.as_view(), name='drf-trade-detail'),
    path('api/v2/drf/trades/<int:trade_id>/images/', TradeImageCreateView.as_view(), name='drf-trade-image-create'),
    path('api/v2/drf/trades/<int:trade_id>/images/<int:image_id>/', TradeImageDestroyView.as_view(), name='drf-trade-image-delete'),
]