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

    def list(self, request, *args, **kwargs):
        root_categories = []     # represents primary_keys only
        serializer_data = {c['id']: c for c in CategoryListSerializer(Category.objects.all(), many=True).data}
        for category_id, category_data in serializer_data.items():
            if category_data['category_id']:
                if serializer_data[category_data['category_id']].get('subcategories') is None:
                    serializer_data[category_data['category_id']]['subcategories'] = [category_id]
                else:
                    serializer_data[category_data['category_id']]['subcategories'].append(category_id)
            else:
                root_categories.append(category_id)
        return Response({"root_categories": root_categories, "categories": serializer_data})


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
