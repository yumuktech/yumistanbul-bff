import uuid

from django.db import models


class District(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class FeatureTag(models.Model):
    key = models.CharField(primary_key=True, max_length=32)
    label = models.CharField(max_length=64)

    class Meta:
        ordering = ['label']

    def __str__(self) -> str:
        return self.label


class AdditionalFilter(models.Model):
    key = models.CharField(primary_key=True, max_length=32)
    label = models.CharField(max_length=64)
    emoji = models.CharField(max_length=8, blank=True)

    class Meta:
        ordering = ['label']

    def __str__(self) -> str:
        return self.label


class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='restaurants')
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    price_tier = models.PositiveSmallIntegerField(default=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    review_count = models.PositiveIntegerField(default=0)
    features = models.ManyToManyField(FeatureTag, blank=True, related_name='restaurants')
    additional_filters = models.ManyToManyField(AdditionalFilter, blank=True, related_name='restaurants')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating', 'name']

    def __str__(self) -> str:
        return self.name
