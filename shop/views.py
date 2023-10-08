from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response

from .models import Category, Good
from .serializers import (
    CategoryCreateSerializer, CategoryListSerializer, CategoryDetailSerializer,
    GoodDetailSerializer, GoodCreateSerializer, GoodListSerializer,

)


class CategoryViewSet(ModelViewSet):

    def get_serializer_class(self):
        sc = None
        if self.action in {"create", "update", "partial_update"}:
            sc = CategoryCreateSerializer
        if sc is None:
            match self.action:
                case "list":
                    sc = CategoryListSerializer
                case "retrieve":
                    sc = CategoryDetailSerializer
                case _:
                    sc = CategoryListSerializer
        return sc

    def get_queryset(self):
        return Category.objects.all().prefetch_related("subcategories", )

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        data = CategoryDetailSerializer(category).data
        if not data['subcategories']:   # pick goods only if there is no other subcategories
            data['goods'] = GoodListSerializer(Good.objects.filter(category_id=category.id), many=True).data
        return Response(data)


class GoodViewSet(RetrieveModelMixin,
                  CreateModelMixin,
                  GenericViewSet):

    def get_queryset(self):
        return Good.objects.all()

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return GoodDetailSerializer
            case "create":
                return GoodCreateSerializer

    def get_object(self):
        good = Good.objects.get(pk=self.kwargs['pk'])
        return good
