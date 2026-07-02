from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Trade, TradeImage
from .serializers_drf import (
    TradeListSerializer,
    TradeDetailSerializer,
    TradeCreateUpdateSerializer,
    TradeImageSerializer
)

class TradeListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.method == 'GET':
            return Trade.objects.filter(status='open')
        return Trade.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TradeCreateUpdateSerializer
        return TradeListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TradeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Trade.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return TradeCreateUpdateSerializer
        return TradeDetailSerializer

class TradeImageCreateView(generics.CreateAPIView):
    serializer_class = TradeImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        trade = get_object_or_404(Trade, pk=self.kwargs['trade_id'])
        serializer.save(author=self.request.user, trade=trade)

class TradeImageDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TradeImage.objects.filter(trade_id=self.kwargs['trade_id'])

    def delete(self, request, *args, **kwargs):
        image = get_object_or_404(TradeImage, pk=self.kwargs['image_id'], trade_id=self.kwargs['trade_id'])
        self.check_object_permissions(request, image)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)