import django_filters

from .models import Restaurant


class RestaurantFilter(django_filters.FilterSet):
    district = django_filters.CharFilter(field_name='district__slug')
    feature = django_filters.CharFilter(method='filter_feature')
    additional = django_filters.CharFilter(method='filter_additional')

    class Meta:
        model = Restaurant
        fields = ['district']

    def filter_feature(self, queryset, name, value):
        values = self.data.getlist(name) if hasattr(self.data, 'getlist') else [value]
        cleaned = [v for v in values if v]
        if not cleaned:
            return queryset
        return queryset.filter(features__key__in=cleaned).distinct()

    def filter_additional(self, queryset, name, value):
        values = self.data.getlist(name) if hasattr(self.data, 'getlist') else [value]
        cleaned = [v for v in values if v]
        if not cleaned:
            return queryset
        return queryset.filter(additional_filters__key__in=cleaned).distinct()
