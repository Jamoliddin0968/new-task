from datetime import timezone
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    OPERATOR = 'operator'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (OPERATOR, 'Operator'),
        (USER, 'User'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


ACTIVE = 'active'
COMPLETED = 'completed'

STATUS_CHOICES = [
    (ACTIVE, 'Active'),
    (COMPLETED, 'Completed'),
]


class Order(models.Model):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    fine_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def calculate_fine(self):
        if self.actual_return_date and self.actual_return_date > self.return_date:
            days_late = (self.actual_return_date - self.return_date).days
            daily_fine = self.book.daily_price * 0.01
            self.fine_amount = days_late * daily_fine
            self.save()

    def calculate_rent(self):
        end_date = self.actual_return_date if self.actual_return_date else timezone.now()
        days_rented = (end_date - self.ordered_date).days or 1

        base_rent = self.book.daily_price * days_rented

        # Agar muddat o'tgan bo'lsa, jarimani hisoblash
        if end_date > self.return_date:
            days_late = (end_date - self.return_date).days
            daily_fine = self.book.daily_price * Decimal('0.01')  # 1% jarima
            self.fine_amount = days_late * daily_fine
        else:
            self.fine_amount = 0

        self.total_amount = base_rent + self.fine_amount
        print(self.total_amount)
        self.save()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = ('user', 'book')
