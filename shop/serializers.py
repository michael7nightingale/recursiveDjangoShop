from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Category, Good


class GoodListSerializer(ModelSerializer):

    class Meta:
        model = Good
        fields = ("id", "name", "category_id")


class CategoryCreateSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "category")


class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name", "category_id")


class CategoryDetailSerializer(ModelSerializer):
    subcategories = SerializerMethodField("get_subcategories")  # categories under at the recursive tree
    super_categories = SerializerMethodField("get_super_categories")  # categories above at the recursive tree
    goods = GoodListSerializer(many=True, default=[])

    class Meta:
        model = Category
        fields = ("id", "name", "category_id", "subcategories", "super_categories", "goods")

    def get_subcategories(self, instance: Category):
        qs = Category.objects.get_subcategories(instance.id)
        return CategoryListSerializer(qs, many=True).data

    def get_super_categories(self, instance: Category):
        qs = Category.objects.get_super_categories(instance.id)
        return CategoryListSerializer(qs, many=True).data


class GoodDetailSerializer(ModelSerializer):
    categories = SerializerMethodField("get_categories")

    class Meta:
        model = Good
        fields = ("id", "name", "categories")

    def get_categories(self, instance: Good):
        qs = Category.objects.get_super_categories(instance.category_id)
        return CategoryListSerializer(qs, many=True).data


class GoodCreateSerializer(ModelSerializer):

    class Meta:
        model = Good
        fields = ("id", "name", "category")
