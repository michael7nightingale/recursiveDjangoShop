from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GoodViewSet


router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("goods", GoodViewSet, basename="good")

urlpatterns = router.urls
