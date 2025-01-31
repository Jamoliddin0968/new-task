from datetime import timedelta

from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from apps.user.api.serializers import (BookSerializer, OrderCreateSerializer,
                                       OrderSerializer, RatingCreateSerializer,
                                       RatingSerializer,
                                       UserCreateUpdateSerializer,
                                       UsersSerializer)
from apps.user.models import Book, Order, Rating, User
from apps.user.permissions import IsAdminUser, IsOperatorUser


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsOperatorUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        book = self.get_object()
        if book.available_copies <= 0:
            return Response(
                {"error": "No copies available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            user=request.user,
            book=book,
            return_date=timezone.now() + timedelta(days=1)
        )

        book.available_copies -= 1
        book.save()

        return Response(OrderSerializer(order).data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('book', 'user')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAdminUser | IsOperatorUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        order: Order = self.get_object()
        if order.status == Order.COMPLETED:
            return Response(
                {"error": "Order is already completed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.actual_return_date = timezone.now()
        order.status = Order.COMPLETED
        order.calculate_rent()
        order.save()

        order.book.available_copies += 1
        order.book.save()

        return Response(OrderSerializer(order).data)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return RatingCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAdminUser]
    serializer_class = UserCreateUpdateSerializer
