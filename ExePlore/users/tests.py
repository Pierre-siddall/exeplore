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
        response = self.c.post('/login/', {'username':'edwinhubble', 'password':'HubbleSpace1990'})
        self.assertRedirects(response, '/home/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_home_page(self):
        # test the home page renders correctly
        response = self.c.get('/home/')
        name = self.user.first_name
        passed_name = response.context['user'].first_name
        self.assertEqual(response.status_code, 200)
        self.assertEqual(name, passed_name)
        self.assertTemplateUsed(response, template_name='registration/home.html')

    def test_settings_page(self):
        # TODO: set a score (when this is implemented)
        level = self.player.get_level()
        response = self.c.get('/settings/')
        passed_level = Player.objects.get(user = response.context['user']).get_level()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(level, passed_level)
        self.assertTemplateUsed(response, template_name='registration/settings.html')
        # TODO: check badges earned (when adding them is implemented)
        # TODO: check visits (when adding them is implemented)

    def test_badges_page(self):
        # TODO: check badges earned (when adding them is implemented)
        self.assertEqual(True, True)
        # self.assertTemplateUsed(response, template_name='registration/badges.html')

    def test_visits_page(self):
        # TODO: check visits (when adding them is implemented)
        self.assertEqual(True, True)
        # self.assertTemplateUsed(response, template_name='registration/locations.html')

    def test_regisration(self):
        # test creation of user using registration
        response = self.c.post('/register/', {'username':'username', 'email':'email@example.com', 'first_name':'first_name', 'last_name':'last_name', 'password1':'complex123', 'password2':'complex123'})
        user = User.objects.get(username='username')
        self.assertEqual(user.username, 'username')
        self.assertRedirects(response, '/home/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)