from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import RecipeViewSet, IngredientViewSet, SubscriptionViewSet
from users.views import UserCreateViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
# router.register(r'users/subscriptions', SubscriptionViewSet, basename='subscripitons')
router.register('users', UserCreateViewSet, basename='users')

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/api-auth/', include('rest_framework.urls')),
    path('v1/', include(router.urls)),
]
