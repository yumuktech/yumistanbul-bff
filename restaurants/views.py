import uuid

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filters import RestaurantFilter
from .models import AdditionalFilter, District, FeatureTag, Restaurant
from .permissions import IsRestaurantEditor
from .serializers import (
    AdditionalFilterSerializer,
    DistrictSerializer,
    FeatureTagSerializer,
    RestaurantDetailSerializer,
    RestaurantListSerializer,
    RestaurantWriteSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = (
        Restaurant.objects.filter(is_active=True)
        .select_related('district')
        .prefetch_related('features', 'additional_filters')
    )
    filterset_class = RestaurantFilter
    permission_classes = [IsRestaurantEditor]
    ordering_fields = ['rating', 'price_tier']
    ordering = ['-rating']

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantListSerializer
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        return RestaurantWriteSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in {'update', 'partial_update', 'destroy'}:
            return Restaurant.objects.select_related('district').prefetch_related(
                'features', 'additional_filters'
            )
        return qs

    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_field, '')
        if not lookup_value:
            return super().get_object()
        base_qs = Restaurant.objects.select_related('district').prefetch_related(
            'features', 'additional_filters'
        )
        try:
            uuid.UUID(str(lookup_value))
        except (ValueError, TypeError):
            obj = get_object_or_404(base_qs, slug=lookup_value)
        else:
            obj = get_object_or_404(base_qs, pk=lookup_value)
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.instance
        read_serializer = RestaurantDetailSerializer(
            instance, context=self.get_serializer_context()
        )
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return self._update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self._update(request, *args, **kwargs)

    def _update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance = serializer.instance
        read_serializer = RestaurantDetailSerializer(
            instance, context=self.get_serializer_context()
        )
        return Response(read_serializer.data)


class FeatureTagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = FeatureTag.objects.all()
    serializer_class = FeatureTagSerializer


class AdditionalFilterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = AdditionalFilter.objects.all()
    serializer_class = AdditionalFilterSerializer


class DistrictViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


@api_view(['GET'])
def search_suggestions(request):
    query = request.query_params.get('q', '').strip()
    restaurants = []
    districts = []
    if query:
        restaurants = (
            Restaurant.objects.filter(Q(name__icontains=query), is_active=True)
            .order_by('name')[:5]
        )
        districts = District.objects.filter(name__icontains=query).order_by('name')[:5]
    payload = {
        'query': query,
        'restaurants': [
            {'id': str(restaurant.id), 'name': restaurant.name, 'slug': restaurant.slug}
            for restaurant in restaurants
        ],
        'districts': [
            {'slug': district.slug, 'name': district.name}
            for district in districts
        ],
    }
    return Response(payload)
