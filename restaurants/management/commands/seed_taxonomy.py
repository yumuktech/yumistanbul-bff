from django.core.management.base import BaseCommand
from django.db import transaction

from restaurants.models import AdditionalFilter, District, FeatureTag

DISTRICTS = [
    {'slug': 'beyoglu', 'name': 'Beyo\u011flu'},
    {'slug': 'kadikoy', 'name': 'Kad\u0131k\u00f6y'},
    {'slug': 'sisli', 'name': '\u015ei\u015fli'},
]

FEATURES = [
    {'key': 'alcohol', 'label': 'Serves Alcohol'},
    {'key': 'outdoor', 'label': 'Outdoor Seating'},
    {'key': 'meal', 'label': 'Full Meals'},
    {'key': 'coffee', 'label': 'Coffee'},
    {'key': 'dessert', 'label': 'Dessert'},
]

ADDITIONAL_FILTERS = [
    {'key': 'date-night', 'label': 'Date Night', 'emoji': '💞'},
    {'key': 'work-friendly', 'label': 'Work Friendly', 'emoji': '💻'},
    {'key': 'group-friendly', 'label': 'Group Friendly', 'emoji': '👥'},
]


class Command(BaseCommand):
    help = 'Seed taxonomy tables with baseline data for the frontend filters.'

    @transaction.atomic
    def handle(self, *args, **options):  # noqa: ARG002
        for district in DISTRICTS:
            District.objects.update_or_create(slug=district['slug'], defaults=district)

        for feature in FEATURES:
            FeatureTag.objects.update_or_create(key=feature['key'], defaults=feature)

        for additional in ADDITIONAL_FILTERS:
            AdditionalFilter.objects.update_or_create(
                key=additional['key'],
                defaults=additional,
            )

        self.stdout.write(self.style.SUCCESS('Seeded taxonomy data.'))
