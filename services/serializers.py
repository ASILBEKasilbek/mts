from rest_framework import serializers
from .models import (
    Category, Price, Image,
    TransportType, TransportBrand, TransportModel,
    CharacteristicValue, Product, Equipment, News, HotOffer, Ad
)
from accounts.serializers import CustomUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["id", "type", "price", "currency"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url"]


class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = ["id", "title", "is_popular", "slug"]


class TransportBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportBrand
        fields = ["id", "title", "is_popular", "slug"]


class TransportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportModel
        fields = ["id", "title", "is_popular", "slug"]


class CharacteristicValueSerializer(serializers.ModelSerializer):
    characteristic = serializers.SerializerMethodField()

    def get_characteristic(self, obj):
        return {"id": obj.characteristic.id, "title": obj.characteristic.title}

    class Meta:
        model = CharacteristicValue
        fields = ["characteristic", "value", "title", "measurement_unit"]


# ---- Base serializer ----
class BaseServiceSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    prices = PriceSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    transport_type = TransportTypeSerializer(read_only=True)
    transport_brand = TransportBrandSerializer(read_only=True)
    transport_model = TransportModelSerializer(read_only=True)
    characteristics = CharacteristicValueSerializer(many=True, read_only=True)
    isNegotiable = serializers.BooleanField(source="is_negotiable", read_only=True)

    class Meta:
        fields = [
            "id", "author", "category", "title", "sub_title", "description",
            "address", "prices", "images", "transport_type", "transport_brand",
            "transport_model", "characteristics", "rank_premium", "rank_search",
            "rank_hot_offer", "slug", "phones", "status", "isNegotiable",
            "stickers", "statistics", "created_at"
        ]


# ---- Child serializers ----
class ProductSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "user", "title", "description", "price", "created_at"]


class EquipmentSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = Equipment


class NewsSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = News
        fields = BaseServiceSerializer.Meta.fields + ["publish_date"]


class HotOfferSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = HotOffer


class AdSerializer(BaseServiceSerializer):
    class Meta(BaseServiceSerializer.Meta):
        model = Ad
        fields = BaseServiceSerializer.Meta.fields + ["duration_days", "is_featured"]
