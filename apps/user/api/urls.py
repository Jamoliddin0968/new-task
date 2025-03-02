from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.user.api.views import BookViewSet, OrderViewSet, RatingViewSet, UsersViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'users', UsersViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
