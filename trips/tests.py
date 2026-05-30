from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

from .models import Trip, Itinerary


class TripModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="sumit",
            password="testpass123"
        )

    def test_trip_creation(self):
        trip = Trip.objects.create(
            user=self.user,
            destination="Goa",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 5),
            total_days=5,
            budget=15000,
            cost_estimate=12000
        )

        self.assertEqual(trip.destination, "Goa")
        self.assertEqual(trip.total_days, 5)

    def test_trip_string_representation(self):
        trip = Trip.objects.create(
            user=self.user,
            destination="Manali",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 7)
        )

        self.assertEqual(str(trip), "Manali Trip")


class ItineraryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="sumit",
            password="testpass123"
        )

        self.trip = Trip.objects.create(
            user=self.user,
            destination="Goa",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 5)
        )

    def test_itinerary_creation(self):
        itinerary = Itinerary.objects.create(
            trip=self.trip,
            day_number=1,
            activity_title="Beach Visit",
            location_address="Baga Beach",
            time_slot="10 AM - 2 PM",
            cost_estimate=1000
        )

        self.assertEqual(itinerary.activity_title, "Beach Visit")
        self.assertEqual(itinerary.status, "Pending")

    def test_itinerary_ordering(self):
        Itinerary.objects.create(
            trip=self.trip,
            day_number=2,
            activity_title="Day 2",
            location_address="Location",
            time_slot="Morning"
        )

        Itinerary.objects.create(
            trip=self.trip,
            day_number=1,
            activity_title="Day 1",
            location_address="Location",
            time_slot="Morning"
        )

        items = list(Itinerary.objects.all())

        self.assertEqual(items[0].day_number, 1)
        self.assertEqual(items[1].day_number, 2)


class RegistrationViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_success(self):
        response = self.client.post(
            reverse("register"),
            {
                "userid": "101",
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "password123",
                "confirm_password": "password123",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )

    def test_register_password_mismatch(self):
        response = self.client.post(
            reverse("register"),
            {
                "userid": "101",
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "password123",
                "confirm_password": "wrongpass",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            User.objects.filter(username="newuser").exists()
        )

    def test_register_short_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "userid": "101",
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "123",
                "confirm_password": "123",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            User.objects.filter(username="newuser").exists()
        )


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="sumit",
            password="password123"
        )

    def test_login_success(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "sumit",
                "password": "password123"
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "sumit",
                "password": "wrongpassword"
            }
        )

        self.assertEqual(response.status_code, 302)


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get(reverse("landing"))

        self.assertEqual(response.status_code, 200)


class BookPackageViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="sumit",
            password="password123"
        )

        self.client.login(
            username="sumit",
            password="password123"
        )

    def test_book_package_page_loads(self):
        response = self.client.get(
            reverse(
                "book_package",
                kwargs={"place_name": "Goa"}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_book_package_post_redirect(self):
        response = self.client.post(
            reverse(
                "book_package",
                kwargs={"place_name": "Goa"}
            ),
            {
                "start_date": "2026-06-01"
            }
        )

        self.assertEqual(response.status_code, 302)