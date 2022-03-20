from django.test import TestCase
from visits.models import Location, Badge
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client

""" Test cases for everything that does not require a player """
class ClientTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_edit_locations(self):
        # test a location can be added
        response = self.c.post('/add_location/', {'location_name':'NEW', 'latitude':10, 'longitude':10, 'point_value':10})
        location = Location.objects.get(location_name='NEW')
        self.assertEqual(location.location_name, 'NEW')
        self.assertRedirects(response, '/settings/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # test that location can be deleted
        response = self.c.post('/del_location/', {'location':location.id})
        with self.assertRaises(ObjectDoesNotExist):
            location = Location.objects.get(location_name='NEW')
        self.assertRedirects(response, '/settings/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_edit_badges(self):
        # test a badge can be added
        response = self.c.post('/add_badge/', {'badge_name':'NEW', 'description':'a new badge', 'tier':'AU'})
        badge = Badge.objects.get(badge_name='NEW')
        self.assertEqual(badge.badge_name, 'NEW')
        self.assertRedirects(response, '/settings/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # test that badge can be deleted
        response = self.c.post('/del_badge/', {'badge':badge.id})
        with self.assertRaises(ObjectDoesNotExist):
            badge = Badge.objects.get(badge_name='NEW')
        self.assertRedirects(response, '/settings/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)