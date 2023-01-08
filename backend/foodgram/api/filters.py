from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):

    is_favorited = filters.BooleanFilter(
        field_name='favorited_by',
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='in_shopping_cart_of',
        method='filter_is_in_shopping_cart'
    )
    tags = filters.MultipleChoiceFilter(
        field_name='tags__slug',
        choices=Tag.objects.values_list('slug', 'slug')
    )
    author = filters.NumberFilter(
        field_name='author__id'
    )

    class Meta:
        model = Recipe
        fields = [
            'favorited_by',
            'in_shopping_cart_of',
            'tags',
            'author'
        ]

    def filter_is_favorited(self, qs, name, value):
        """
        Фильтрация в зависимости от значения поля модели Recipe:
        favorited_by.
        """

        return (
            qs.filter(favorited_by=self.request.user.id) if value
            else qs.exclude(favorited_by=self.request.user.id)
        )

    def filter_is_in_shopping_cart(self, qs, name, value):
        """
        Фильтрация в зависимости от значения поля модели Recipe:
        in_shopping_cart_of.
        """

        return (
            qs.filter(in_shopping_cart_of=self.request.user.id) if value
            else qs.exclude(in_shopping_cart_of=self.request.user.id)
        )
