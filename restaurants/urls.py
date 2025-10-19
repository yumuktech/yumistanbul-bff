from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdditionalFilterViewSet,
    DistrictViewSet,
    FeatureTagViewSet,
    RestaurantViewSet,
    search_suggestions,
)

router = DefaultRouter()
router.register('restaurants', RestaurantViewSet, basename='restaurant')
router.register('features', FeatureTagViewSet, basename='feature')
router.register('additional-filters', AdditionalFilterViewSet, basename='additional-filter')
router.register('districts', DistrictViewSet, basename='district')

urlpatterns = [
    path('', include(router.urls)),
    path('search/suggestions/', search_suggestions, name='search-suggestions'),
]
