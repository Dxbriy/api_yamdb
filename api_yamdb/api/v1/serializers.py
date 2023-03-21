import datetime as dt

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class ValidateUserSerializer:
    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        if username and username.lower() == 'me':
            raise serializers.ValidationError(
                'Пользователь me не может быть создан и изменен'
            )
        # second condition hanldes case, when we validate the already
        # created user with the same attrs - when he should get only
        # confirmation
        # without it test failed with:
        # Проверьте, что повторный POST-запрос к `/api/v1/auth/signup/`
        # с данными зарегистрированного пользователя возвращает ответ
        # со статусом 200
        if (
            User.objects.filter(username=username).exists()
            and not User.objects.filter(**attrs).exists()
        ):
            raise serializers.ValidationError('Пользователь уже существует')
        if (
            User.objects.filter(email=email).exists()
            and not User.objects.filter(**attrs).exists()
        ):
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже существует'
            )
        return attrs


class UserSerializer(ValidateUserSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('confirmation_code', 'username')


class RegisterSerializer(ValidateUserSerializer, serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        required=True,
        max_length=settings.MID_SMALL_INT_LENGTH,
    )
    email = serializers.EmailField(
        required=True,
        max_length=settings.BIG_INT_LENGTH,
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=True,
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError('Нельзя указать будущий год')
        if value < 0:
            raise serializers.ValidationError(
                'Нельзя указать отлрицательный год'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        exclude = ('review',)
        read_only_fields = ('id', 'review', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        exclude = ('title',)
        read_only_fields = ('id', 'title', 'pub_date')
        model = Review

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале')
        return value

    @staticmethod
    def check_only_one_review(review):
        if review:
            raise serializers.ValidationError(
                'Может оставить только один отзыв'
            )
