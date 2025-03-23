from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from api.models import Workshop, Reservation, Review
from datetime import timedelta

class APIPassTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.workshop = Workshop.objects.create(
            owner=self.user,
            name="Test Workshop",
            description="Test Desc",
            location="Test City",
            area=100.0,
            equipment="Tools",
            hourly_rate=10.0,
            daily_rate=100.0,
            monthly_rate=1000.0,
            rental_terms="Terms apply"
        )

    def test_user_can_register(self):
        response = self.client.post('/api/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'securepass123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('user_id', response.data)

    def test_user_can_create_workshop(self):
        response = self.client.post('/api/workshops/', {
            'name': 'New Workshop',
            'description': 'Great place',
            'location': 'Warsaw',
            'area': 50,
            'equipment': 'Hammer, Wrench',
            'hourly_rate': 20.0,
            'daily_rate': 150.0,
            'monthly_rate': 2000.0,
            'rental_terms': 'Respect the space'
        })
        self.assertEqual(response.status_code, 201)

    def test_user_can_make_reservation(self):
        start = timezone.now() + timezone.timedelta(days=1)
        end = start + timezone.timedelta(hours=2)
        response = self.client.post('/api/reservations/', {
            'workshop': self.workshop.id,
            'start_datetime': start.isoformat(),
            'end_datetime': end.isoformat()
        })
        self.assertEqual(response.status_code, 201)

    def test_user_can_review_after_reservation(self):
        start = timezone.now() - timezone.timedelta(days=2)
        end = timezone.now() - timezone.timedelta(days=1)
        Reservation.objects.create(
            workshop=self.workshop,
            renter=self.user,
            start_datetime=start,
            end_datetime=end,
            total_price=100
        )
        response = self.client.post('/api/reviews/', {
            'workshop': self.workshop.id,
            'rating': 5,
            'comment': 'Super warsztat!'
        })
        self.assertEqual(response.status_code, 201)

class APIFunctionalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.workshop = Workshop.objects.create(
            owner=self.user,
            name="Test Workshop",
            description="Opis",
            location="Wrocław",
            area=50,
            equipment="Szlifierka, stół",
            hourly_rate=20.0,
            daily_rate=150.0,
            monthly_rate=2000.0,
            rental_terms="Bez bałaganu"
        )

    def test_register_user(self):
        response = self.client.post('/api/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'strongpass123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('user_id', response.data)

    def test_create_workshop(self):
        response = self.client.post('/api/workshops/', {
            'name': 'Nowy Warsztat',
            'description': 'Opis testowy',
            'location': 'Gdańsk',
            'area': 60,
            'equipment': 'Młotek, wiertarka',
            'hourly_rate': 25,
            'daily_rate': 180,
            'monthly_rate': 2500,
            'rental_terms': 'Testowe warunki'
        })
        self.assertEqual(response.status_code, 201)

    def test_valid_reservation(self):
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)
        response = self.client.post('/api/reservations/', {
            'workshop': self.workshop.id,
            'start_datetime': start.isoformat(),
            'end_datetime': end.isoformat()
        })
        self.assertEqual(response.status_code, 201)

    def test_review_after_reservation(self):
        start = timezone.now() - timedelta(days=2)
        end = timezone.now() - timedelta(days=1)
        Reservation.objects.create(
            workshop=self.workshop,
            renter=self.user,
            start_datetime=start,
            end_datetime=end,
            total_price=50
        )
        response = self.client.post('/api/reviews/', {
            'workshop': self.workshop.id,
            'rating': 4,
            'comment': 'Bardzo dobrze!'
        })
        self.assertEqual(response.status_code, 201)

    def test_cannot_reserve_in_past(self):
        start = timezone.now() - timedelta(days=1)
        end = timezone.now()
        response = self.client.post('/api/reservations/', {
            'workshop': self.workshop.id,
            'start_datetime': start.isoformat(),
            'end_datetime': end.isoformat()
        })
        self.assertEqual(response.status_code, 400)


    def test_cannot_review_twice(self):
        start = timezone.now() - timedelta(days=3)
        end = timezone.now() - timedelta(days=2)
        Reservation.objects.create(
            workshop=self.workshop,
            renter=self.user,
            start_datetime=start,
            end_datetime=end,
            total_price=60
        )
        self.client.post('/api/reviews/', {
            'workshop': self.workshop.id,
            'rating': 5,
            'comment': 'Pierwszy komentarz'
        })
        response = self.client.post('/api/reviews/', {
            'workshop': self.workshop.id,
            'rating': 4,
            'comment': 'Drugi raz'
        })
        self.assertEqual(response.status_code, 400)

    def test_workshop_list(self):
        response = self.client.get('/api/workshops/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)