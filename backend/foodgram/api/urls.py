from django.urls import include, path
from rest_framework import routers
from users.views import CustomUserSubscriptionViewSet

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

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
