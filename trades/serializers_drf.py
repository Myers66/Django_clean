from rest_framework import serializers
from .models import Trade, TradeImage, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone')

class TradeImageSerializer(serializers.ModelSerializer):
    delete_url = serializers.SerializerMethodField()

    class Meta:
        model = TradeImage
        fields = ('id', 'image', 'created_at', 'updated_at', 'delete_url')
        read_only_fields = ('author', 'trade')

    def get_delete_url(self, obj):
        return f"/api/v2/drf/trades/{obj.trade.id}/images/{obj.id}/"

class TradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('id', 'title', 'created_at')

class TradeDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    images = TradeImageSerializer(many=True, read_only=True)
    images_url = serializers.SerializerMethodField()

    class Meta:
        model = Trade
        fields = ('id', 'title', 'description', 'status',
                  'created_at', 'updated_at', 'author', 'images', 'images_url')

    def get_images_url(self, obj):
        return f"/api/v2/drf/trades/{obj.id}/images/"

class TradeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('title', 'description', 'status')