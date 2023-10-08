from django.urls import path, include


urlpatterns = [
    path("shop/", include("shop.urls")),

]
