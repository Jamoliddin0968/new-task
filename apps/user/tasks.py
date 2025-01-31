from celery import shared_task
from django.utils import timezone

from .models import ACTIVE, Book, Order


@shared_task
def check_status_orders():
    expired_orders = Order.objects.filter(
        status=ACTIVE,
        ordered_date__lt=timezone.now() - timezone.timedelta(days=1),
        actual_return_date__isnull=True
    )

    for order in expired_orders:
        order.is_active = False
        order.save()

        book = order.book
        book.available_copies += 1
        book.save()

    active_orders = Order.objects.filter(
        status=ACTIVE
    )

    for order in active_orders:
        order.calculate_rent()
