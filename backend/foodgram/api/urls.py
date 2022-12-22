from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (
    RecipeViewSet, IngredientViewSet, TagViewSet
)
from users.views import CustomUserSubscriptionViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register('users', CustomUserSubscriptionViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
