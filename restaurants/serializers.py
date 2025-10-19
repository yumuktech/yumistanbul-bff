from rest_framework import serializers

from .models import AdditionalFilter, District, FeatureTag, Restaurant


class FeatureTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureTag
        fields = ['key', 'label']


class AdditionalFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalFilter
        fields = ['key', 'label', 'emoji']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['slug', 'name']


class RestaurantListSerializer(serializers.ModelSerializer):
    district = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    district_name = serializers.CharField(source='district.name', read_only=True)
    features = serializers.SlugRelatedField(many=True, read_only=True, slug_field='key')
    additional_filters = serializers.SlugRelatedField(many=True, read_only=True, slug_field='key')

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'slug',
            'district',
            'district_name',
            'price_tier',
            'rating',
            'review_count',
            'features',
            'additional_filters',
        ]


class RestaurantDetailSerializer(RestaurantListSerializer):
    class Meta(RestaurantListSerializer.Meta):
        fields = RestaurantListSerializer.Meta.fields + [
            'description',
            'address',
            'latitude',
            'longitude',
            'created_at',
            'updated_at',
        ]


class RestaurantWriteSerializer(serializers.ModelSerializer):
    feature_keys = serializers.ListField(
        child=serializers.CharField(max_length=32), write_only=True, required=False
    )
    additional_keys = serializers.ListField(
        child=serializers.CharField(max_length=32), write_only=True, required=False
    )

    class Meta:
        model = Restaurant
        fields = [
            'name',
            'slug',
            'district',
            'description',
            'address',
            'latitude',
            'longitude',
            'price_tier',
            'feature_keys',
            'additional_keys',
            'is_active',
        ]

    def validate_price_tier(self, value: int) -> int:
        if value < 1 or value > 4:
            raise serializers.ValidationError('price_tier must be between 1 and 4')
        return value

    def create(self, validated_data):
        feature_keys = validated_data.pop('feature_keys', [])
        additional_keys = validated_data.pop('additional_keys', [])
        restaurant = Restaurant.objects.create(**validated_data)
        if feature_keys:
            restaurant.features.set(self._get_related_features(feature_keys, 'feature_keys'))
        if additional_keys:
            restaurant.additional_filters.set(
                self._get_related_additional(additional_keys, 'additional_keys')
            )
        return restaurant

    def update(self, instance, validated_data):
        feature_keys = validated_data.pop('feature_keys', None)
        additional_keys = validated_data.pop('additional_keys', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if feature_keys is not None:
            instance.features.set(self._get_related_features(feature_keys, 'feature_keys'))
        if additional_keys is not None:
            instance.additional_filters.set(
                self._get_related_additional(additional_keys, 'additional_keys')
            )
        return instance

    def _get_related_features(self, keys, field_name):
        return self._resolve_related(FeatureTag, keys, field_name)

    def _get_related_additional(self, keys, field_name):
        return self._resolve_related(AdditionalFilter, keys, field_name)

    def _resolve_related(self, model, keys, field_name):
        unique_keys = list(dict.fromkeys(keys))
        matches = list(model.objects.filter(key__in=unique_keys))
        found_keys = {item.key for item in matches}
        missing = [key for key in unique_keys if key not in found_keys]
        if missing:
            raise serializers.ValidationError({field_name: f'Unknown keys: {", ".join(missing)}'})
        return matches
