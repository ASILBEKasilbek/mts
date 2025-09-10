# services/views.py
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import AdSerializer
from .models import Product, Equipment, News, HotOffer,Ad
from .serializers import (
    ProductSerializer, EquipmentSerializer, NewsSerializer, HotOfferSerializer
)
from accounts.permissions import IsBusinessOrAdmin

# 🔹 Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# 🔹 Product Views
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category", "status"]
    search_fields = ["title", "description"]

    @swagger_auto_schema(operation_description="Barcha mahsulotlarni olish.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PaginatedProductList(ProductList):
    pagination_class = StandardResultsSetPagination


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsBusinessOrAdmin()]
        return [IsAuthenticated()]


@method_decorator(ratelimit(key="ip", rate="5/m", method="POST", block=True), name="dispatch")
class ProductIncrementView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Ko‘rish sonini oshirish.")
    def post(self, request, id):
        product = Product.objects.get(id=id)
        product.increment_view()
        product.statistics["clicked"] = product.statistics.get("clicked", 0) + 1
        product.save()
        return Response({"status": "success"})


class ProductToggleLike(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Like bosish yoki o‘chirish.")
    def post(self, request, id):
        product = Product.objects.get(id=id)
        product.toggle_like(request.user)
        return Response({"status": "toggled"})


# 🔹 Equipment Views
class EquipmentList(generics.ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class PaginatedEquipmentList(EquipmentList):
    pagination_class = StandardResultsSetPagination


class EquipmentIncrementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        equipment = Equipment.objects.get(id=id)
        equipment.increment_view()
        equipment.save()
        return Response({"status": "success"})


# 🔹 News Views
class NewsList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class PaginatedNewsList(NewsList):
    pagination_class = StandardResultsSetPagination


class NewsDetail(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = "id"


class NewsIncrementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        news = News.objects.get(id=id)
        news.increment_view()
        news.save()
        return Response({"status": "success"})


# 🔹 HotOffer Views
class HotOfferList(generics.ListAPIView):
    queryset = HotOffer.objects.filter(rank_hot_offer=True)
    serializer_class = HotOfferSerializer


class PaginatedHotOfferList(HotOfferList):
    pagination_class = StandardResultsSetPagination


class HotOfferDetail(generics.RetrieveAPIView):
    queryset = HotOffer.objects.all()
    serializer_class = HotOfferSerializer
    lookup_field = "slug"


# 🔹 Edit Product
class EditProduct(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    permission_classes = [IsBusinessOrAdmin]



class AdDetail(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    lookup_field = "slug"