from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.models import AdditionalFilter, District, FeatureTag, Restaurant


class RestaurantAPITestCase(APITestCase):
    def setUp(self):
        self.district = District.objects.create(name='Beyoğlu', slug='beyoglu')
        self.feature = FeatureTag.objects.create(key='outdoor', label='Outdoor Seating')
        self.additional = AdditionalFilter.objects.create(
            key='date-night', label='Date Night', emoji=''
        )
        self.restaurant = Restaurant.objects.create(
            name='Mikla',
            slug='mikla',
            district=self.district,
            price_tier=3,
            rating=4.5,
            review_count=100,
        )
        self.restaurant.features.add(self.feature)
        self.restaurant.additional_filters.add(self.additional)

    def test_list_restaurants_anonymous(self):
        url = reverse('restaurant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['results'][0]['slug'], 'mikla')

    def test_filter_by_district_and_feature(self):
        url = reverse('restaurant-list')
        response = self.client.get(url, {'district': 'beyoglu', 'feature': 'outdoor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()
        self.assertEqual(payload['count'], 1)

        response = self.client.get(url, {'district': 'unknown', 'feature': 'outdoor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 0)

    def test_editor_can_create_restaurant(self):
        url = reverse('restaurant-list')
        payload = {
            'name': 'Yeni Mekan',
            'slug': 'yeni-mekan',
            'district': self.district.pk,
            'price_tier': 2,
            'feature_keys': ['outdoor'],
            'additional_keys': ['date-night'],
            'is_active': True,
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        editors = Group.objects.create(name='editors')
        user = User.objects.create_user(username='editor', password='pass12345')
        user.groups.add(editors)

        self.client.force_authenticate(user=user)
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_search_suggestions_shape(self):
        url = reverse('search-suggestions')
        response = self.client.get(url, {'q': 'mik'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()
        self.assertEqual(payload['query'], 'mik')
        self.assertEqual(len(payload['restaurants']), 1)
