from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Dietitian, PracticeLocation, User


class DietitianModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='johndoe', password='12345')
        self.dietitian = Dietitian.objects.create(user=self.user, phone_number='1234567890',
                                                  country_of_practice='Gotham')

    def test_dietitian_not_approved_sets_locations_not_approved(self):
        self.dietitian.is_approved = True
        self.dietitian.save()

        location1 = PracticeLocation.objects.create(dietitian=self.dietitian, address='123 Test St',
                                                    phone_number=456, is_approved=True)
        location2 = PracticeLocation.objects.create(dietitian=self.dietitian, address='456 Test Ave',
                                                    phone_number=123, is_approved=True)

        self.dietitian.is_approved = False
        self.dietitian.save()

        location1.refresh_from_db()
        location2.refresh_from_db()

        self.assertFalse(location1.is_approved)
        self.assertFalse(location2.is_approved)

    def test_dietitian_approved_does_not_set_locations_approved(self):
        self.dietitian.is_approved = True
        self.dietitian.save()

        location1 = PracticeLocation.objects.create(dietitian=self.dietitian, address='123 Test St', latitude=1.0,
                                                    longitude=1.0, is_approved=False)
        location2 = PracticeLocation.objects.create(dietitian=self.dietitian, address='456 Test Ave', latitude=2.0,
                                                    longitude=2.0, is_approved=False)

        self.assertFalse(location1.is_approved)
        self.assertFalse(location2.is_approved)

    def test_cannot_approve_location_if_dietitian_not_approved(self):
        with self.assertRaises(ValidationError):
            location = PracticeLocation(dietitian=self.dietitian, address='123 Test St', latitude=1.0, longitude=1.0,
                                        is_approved=True)
            location.save()


class PracticeLocationModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='johndoe', password='12345')
        self.dietitian = Dietitian.objects.create(user=self.user, phone_number='1234567890',
                                                  country_of_practice='Gotham')

    def test_max_locations_limit(self):
        self.dietitian.max_locations = 2
        self.dietitian.save()

        PracticeLocation.objects.create(dietitian=self.dietitian, address='123 Test St')
        PracticeLocation.objects.create(dietitian=self.dietitian, address='456 Test Ave')

        with self.assertRaises(ValidationError):
            PracticeLocation.objects.create(dietitian=self.dietitian, address='789 Test Blvd')
