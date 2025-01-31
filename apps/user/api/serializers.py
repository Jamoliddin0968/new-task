from rest_framework import serializers

from apps.user.models import Book, Order, Rating, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "username", "first_name", "last_name", "email", "role"
        )


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    book = BookSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('fine_amount',)


class OrderCreateSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    book = BookSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('fine_amount',)


class RatingSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Rating
        fields = '__all__'


class RatingCreateSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Rating
        fields = '__all__'


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=3)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",

            "role",
            "groups",
            "password"
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        if 'password' in validated_data.keys():
            instance.set_password(validated_data['password'])
            instance.save()
        return instance

    def update(self, instance: User, validated_data):
        instance = super().update(instance, validated_data)
        if 'password' in validated_data.keys():
            instance.set_password(validated_data['password'])
            instance.save()
        return instance
