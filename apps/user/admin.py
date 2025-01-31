from django.contrib import admin

from apps.user.models import Book, Order, Rating, User

admin.site.register((User, Book, Order, Rating))
