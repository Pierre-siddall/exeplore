from django.test import RequestFactory, TestCase
from users.models import Player, EarnedBadge, Visit
from visits.models import Location, Badge
from django.test import Client
from Exeplore.views import login_view
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

""" Test cases for everything that requires a player """
class ClientTestCase(TestCase):
    def setUp(self):
        # create a user as a player
        self.user = User.objects.create_user('edwinhubble', None, 'HubbleSpace1990', first_name='Edwin', last_name='Hubble')
        self.group = Group.objects.create(name = 'Player')
        self.user.groups.add(self.group)
        self.player = Player.objects.get(user = self.user)
        # make two locations
        self.location = Location.objects.create(location_name='location', latitude=10.0, longitude=20.0, point_value=30)
        self.location2 = Location.objects.create(location_name='second', latitude=10.0, longitude=20.0, point_value=10)
        # make two badges
        self.badge = Badge.objects.create(badge_name='badge', description='', tier='AU')
        self.badge2 = Badge.objects.create(badge_name='second', description='', tier='PT')
        # make a visit
        self.visit = Visit.objects.create(player=self.player, location=self.location2, visit_datetime='')
        self.player.set_score(self.location2)
        self.player.save()
        # make an earned badge
        self.earned = EarnedBadge.objects.create(player=self.player, badge=self.badge2, badge_earned_datetime='')
        # create a session cookie
        self.c = Client()
        self.session = self.c.session
        self.session['username'] = 'edwinhubble'
        self.session.save()

    def test_user_login(self):
        # test the user can be logged in
        response = self.c.post('/login/', {'username':'edwinhubble', 'password':'HubbleSpace1990'})
        self.assertRedirects(response, '/home/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_home_page(self):
        # call the home page
        response = self.c.get('/home/')
        name = self.user.first_name
        passed_name = response.context['user'].first_name
        # check the home page renders
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/home.html')
        # check the correct values were passed
        self.assertEqual(name, passed_name)
        self.assertEqual([10.0, 10.0], response.context['lats'])
        self.assertEqual([20.0, 20.0], response.context['lngs'])

    def test_settings_page(self):
        response = self.c.get('/settings/')
        # get passed values
        passed_level = Player.objects.get(user = response.context['user']).get_level()
        passed_visits = list(response.context['visits'])
        passed_ebs = list(response.context['earnedBadges'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, passed_level)
        self.assertTemplateUsed(response, template_name='registration/settings.html')
        # check the user's earned badges
        self.assertEqual(passed_ebs, [self.earned])
        # check the user's visits
        self.assertEqual(passed_visits, [self.visit])

    def test_gk_permissions(self):
        # make the user a gamekeeper
        group = Group.objects.create(name = 'Gamekeeper')
        self.user.groups.add(group)
        # player = Player.objects.get(user = self.user)
        # call the settings page
        response = self.c.get('/settings/')
        self.assertEqual(response.status_code, 200)
        # check the permission was passed correctly
        self.assertEqual(response.context['permission'], True)
        self.assertEqual(response.context['developer'], False)
        self.assertTemplateUsed(response, template_name='registration/settings.html')

    def test_dev_permissions(self):
        # make the user a developer
        group = Group.objects.create(name = 'Developer')
        self.user.groups.add(group)
        # player = Player.objects.get(user = self.user)
        # call the settings page
        response = self.c.get('/settings/')
        self.assertEqual(response.status_code, 200)
        # check the permission was passed correctly
        self.assertEqual(response.context['permission'], True)
        self.assertEqual(response.context['developer'], True)
        self.assertTemplateUsed(response, template_name='registration/settings.html')

    def test_edit_users(self):
        # test a user can be added
        response = self.c.post('/add_user/', {'username':'new', 'first_name':'new', 'last_name':'new', 'email':'new@exeter.ac.uk', 'password1':'user1234', 'password2':'user1234', 'group':'Player'})
        user = User.objects.get(username='new')
        self.assertEqual(user.username, 'new')
        self.assertEqual(user.groups.filter(name='Gamekeeper').exists(), False)
        self.assertEqual(user.groups.filter(name='Player').exists(), True)
        self.assertRedirects(response, '/settings/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # test that user can be made a gamekeeper
        Group.objects.create(name = 'Gamekeeper')
        response = self.c.post('/edit_user/', {'user':user.id, 'group':'Gamekeeper', 'action':'add'})
        self.assertEqual(user.groups.filter(name='Gamekeeper').exists(), True)
        self.assertEqual(user.groups.filter(name='Player').exists(), True)
        self.assertRedirects(response, '/settings/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # test that user can be removed from the player group
        response = self.c.post('/edit_user/', {'user':user.id, 'group':'Player', 'action':'remove'})
        self.assertEqual(user.groups.filter(name='Gamekeeper').exists(), True)
        self.assertEqual(user.groups.filter(name='Player').exists(), False)
        self.assertRedirects(response, '/settings/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # test that user can be deleted
        response = self.c.post('/del_user/', {'user':user.id})
        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(username='new')
        self.assertRedirects(response, '/settings/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_badges_page(self):
        response = self.c.get('/badges/')
        # get the lists of earned and unearned badges
        passed_badges = list(response.context['badges'])
        passed_earned = list(response.context['earnedBadges'])
        # check the page runs correctly
        self.assertTemplateUsed(response, template_name='registration/badges.html')
        self.assertEqual(passed_badges, [self.badge])
        self.assertEqual(passed_earned, [self.badge2])

    def test_locations_page(self):
        response = self.c.get('/locations/')
        # get the lists of earned and unearned badges
        passed_locations = list(response.context['locations'])
        passed_visits = list(response.context['visits'])
        # check the page runs correctly
        self.assertTemplateUsed(response, template_name='registration/locations.html')
        self.assertEqual(passed_locations, [self.location])
        self.assertEqual(passed_visits, [self.location2])

    def test_regisration(self):
        # test creation of user using registration
        response = self.c.post('/register/', {'username':'username', 'email':'email@example.com', 'first_name':'first_name', 'last_name':'last_name', 'password1':'complex123', 'password2':'complex123'})
        user = User.objects.get(username='username')
        self.assertEqual(user.username, 'username')
        self.assertRedirects(response, '/home/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_user_logout(self):
        # test logging out, including cookie is deleted
        response = self.c.get('/logout/')
        self.assertRedirects(response, '/splash/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.session = self.c.session
        with self.assertRaises(KeyError):
            username = self.session['username']

    def test_scan_location(self):
        response = self.c.post('/scanning/', {'location':'location', 'answer':'1', 'radio':'1'})
        self.assertRedirects(response, '/locations/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # get the visits currently set
        visits = Visit.objects.filter(player=self.player)
        locations = []
        for v in visits:
            # get the locations of those visits
            locations.append(v.location)
        # check the locations have been recorded as visited
        self.assertEqual(locations, [self.location2, self.location])