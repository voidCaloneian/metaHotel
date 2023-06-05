from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse

from .models import MetaHotel, Hotel, HotelHistory


class TestHotelViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.hotel_data = {'name': 'Test hotel'}
    
    def test_create_hotel(self):
        url = reverse('hotel-list')
        
        response = self.client.post(url, self.hotel_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hotel.objects.count(), 1)
        self.assertEqual(Hotel.objects.get().name, 'Test hotel')
        
    def test_update_hotel_meta_hotel(self):
        meta_hotel = MetaHotel.objects.create(id='test-meta-hotel')
        hotel = Hotel.objects.create(name='Test hotel')
        
        url = reverse('hotel-detail', args=[hotel.pk])
        data = {'meta_hotel': meta_hotel.pk}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Hotel.objects.get(pk=hotel.pk).meta_hotel, meta_hotel)
    
    def test_retrieve_hotel_history(self):
        meta_hotel = MetaHotel.objects.create(id='test-meta-hotel')
        hotel = Hotel.objects.create(name='Test hotel', meta_hotel=meta_hotel)
        
        url = reverse('hotel-detail', args=[hotel.pk])
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta_hotel'], meta_hotel.id)
        self.assertIn('history', response.data)
        self.assertEqual(len(response.data['history']), 1)

class TestMetaHotelViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('metahotel-list')
    
    def test_list_meta_hotels(self):
        meta_hotel = MetaHotel.objects.create(id='test-meta-hotel')
        hotel = Hotel.objects.create(name='Test hotel', meta_hotel=meta_hotel)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], meta_hotel.id)
        self.assertIn('hotels', response.data[0])
        self.assertEqual(len(response.data[0]['hotels']), 1)
        self.assertEqual(response.data[0]['hotels'][0]['name'], hotel.name)

class TestBindHotelsAPIView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.meta_hotel = MetaHotel.objects.create(id='test-meta-hotel')
        self.hotel1 = Hotel.objects.create(name='Test hotel 1')
        self.hotel2 = Hotel.objects.create(name='Test hotel 2')
        self.url = reverse('bind-hotels')
    
    def test_bind_hotels(self):
        data = {'hotels_pks': f"{self.hotel1.pk},{self.hotel2.pk}", 'meta_hotel': self.meta_hotel.pk}
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Hotel.objects.filter(meta_hotel=self.meta_hotel).count(), 2)
        self.assertTrue(HotelHistory.objects.filter(hotel=self.hotel1, meta_hotel=self.meta_hotel).exists())
        self.assertTrue(HotelHistory.objects.filter(hotel=self.hotel2, meta_hotel=self.meta_hotel).exists())
