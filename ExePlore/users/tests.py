from django.test import RequestFactory, TestCase
from users.models import Player
from django.test import Client
from Exeplore.views import login_view
from django.contrib.auth.models import User, Group

class ClientTestCase(TestCase):
    def setUp(self):
        # create a user
        self.user = User.objects.create_user('edwinhubble', None, 'HubbleSpace1990', first_name='Edwin', last_name='Hubble')
        # make them a player
        self.group = Group.objects.create(name = 'Player')
        self.user.groups.add(self.group)
        # get the player object too
        self.player = Player.objects.get(user = self.user)
        self.c = Client()
        # create a session cookie
        self.session = self.c.session
        self.session['username'] = 'edwinhubble'
        self.session.save()

    def test_user_login(self):
        # test the user can be logged in
        response = self.c.login(username='edwinhubble', password='HubbleSpace1990')
        self.assertEqual(response, True)

    def test_home_page(self):
        # test the home page renders correctly
        response = self.c.get('/home/')
        name = self.user.first_name
        passed_name = response.context['user'].first_name
        self.assertEqual(response.status_code, 200)
        self.assertEqual(name, passed_name)

    def test_settings_page(self):
        # TODO: set a score (when this is implemented)
        level = self.player.get_level()
        response = self.c.get('/settings/')
        passed_level = Player.objects.get(user = response.context['user']).get_level()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(level, passed_level)
        # TODO: check badges earned (when adding them is implemented)
        # TODO: check visits (when adding them is implemented)

    def test_badges_page(self):
        # TODO: check badges earned (when adding them is implemented)
        # TODO: check list of badges

    def test_visits_page(self):
        # TODO: check visits (when adding them is implemented)
        # TODO: check list of locations

    def test_regisration(self):
        # TODO: creation of user using registration