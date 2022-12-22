from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe


class RecipeFilter(FilterSet):

    is_favorited = filters.BooleanFilter(
        field_name='favorited_by',
        method='filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='in_shopping_cart_of',
        method='filter'
    )
    tags = filters.CharFilter(field_name='tags__slug', lookup_expr='icontains')
    author = filters.NumberFilter(field_name='author__id')

    class Meta:
        model = Recipe
        fields = ['favorited_by', 'in_shopping_cart_of']

    def filter(self, qs, name, value):
        """
        Фильтрация в зависимости от значения полей модели Recipe:
        favorited_by / in_shopping_cart_of.
        """

        return qs.filter(name=self.request.user) if value \
            else qs.exclude(name=self.request.user)
