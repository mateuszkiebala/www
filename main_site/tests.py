from django.test import TestCase, Client
from .models import Commune, Province, Candidate, Voting
import json
import urllib
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.test import LiveServerTestCase
from selenium import webdriver


def create_province(name):
    Province.objects.create(name=name)


def get_province(name):
    return Province.objects.filter(name=name)[0]


def create_commune(comm):
    Commune.objects.create(name=comm['name'], province=comm['province'])


def get_commune(name, province):
    return Commune.objects.filter(name=name, province=province)[0]


def create_candidate(name, surname):
    Candidate.objects.create(name=name, surname=surname)


def get_candidate(name, surname):
    return Candidate.objects.filter(name=name, surname=surname)[0]


def create_voting(candidate, commune, votes):
    Voting.objects.create(candidate=candidate, commune=commune, votes=votes)


def get_votes(candidate, commune):
    return Voting.objects.filter(candidate=candidate, commune=commune)[0].votes


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urllib.urlencode(get)
    return url


def my_login(username):
    user = User.objects.create(username=username)
    user.set_password('12345')
    user.save()
    c = Client()
    c.login(username=username, password='12345')
    return c


class UpdateResults(TestCase):
    def test_wrong_data(self):
        province_name = "AA"
        commune_name = "A"
        create_province(province_name)
        comm = {'name': commune_name, 'province': get_province(province_name), 'inhabitants': 9000,
                'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                'votes': 6000, 'valid_votes': 5000}
        create_commune(comm)

        c = my_login("user_1")
        create_candidate("Lech", "A")
        create_candidate("Donald", "B")
        to_send = {'commune': commune_name, 'province_name': province_name, 'inhabitants': 9000,
                   'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 5000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 4500, 'candidate_1_votes': 2500}
        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertEqual(ret.status_code, 500)

        ret = c.get('/api/update_results/', to_send, content_type="application/json")
        self.assertEqual(ret.status_code, 405)

        to_send = {'commune': commune_name, 'province_name': province_name, 'inhabitants': 9000,
                   'entitled_inhabitants': 10000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 5000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 2500, 'candidate_1_votes': 2500}

        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertNotEqual(ret.status_code, 200)

        to_send = {'commune': commune_name, 'province_name': province_name, 'inhabitants': 9000,
                   'entitled_inhabitants': 9000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 7000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 2500, 'candidate_1_votes': 2500}

        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertNotEqual(ret.status_code, 200)

        to_send = {'commune': commune_name, 'province_name': province_name, 'inhabitants': 9000,
                   'entitled_inhabitants': 9000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 7000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 2500, 'candidate_1_votes': 2500}

        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertNotEqual(ret.status_code, 200)

        to_send = {'commune': commune_name, 'province_name': "", 'inhabitants': 9000,
                   'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 5000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 2500, 'candidate_1_votes': 2500}

        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertNotEqual(ret.status_code, 200)

        to_send = {'commune': "", 'province_name': province_name, 'inhabitants': 9000,
                   'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 5000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 2500, 'candidate_1_votes': 2500}
        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertNotEqual(ret.status_code, 200)

    def test_update(self):
        province_name = "AA"
        commune_name = "A"
        create_province(province_name)
        comm = {'name': commune_name, 'province': get_province(province_name), 'inhabitants': 9000,
                'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                'votes': 6000, 'valid_votes': 5000}
        create_commune(comm)

        c = my_login("user_1")
        create_candidate("Lech", "A")
        create_candidate("Donald", "B")
        commune = get_commune(commune_name, get_province(province_name))
        candidate_0 = get_candidate("Lech", "A")
        candidate_1 = get_candidate("Donald", "B")
        create_voting(candidate_0, commune, 2500)
        create_voting(candidate_1, commune, 2500)

        to_send = {'commune': commune_name, 'province_name': province_name, 'inhabitants': 9000,
                   'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 5000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 3500, 'candidate_1_votes': 1500}
        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertEqual(ret.status_code, 200)
        commune = get_commune(commune_name, get_province(province_name))
        self.assertEqual(get_votes(candidate_0, commune), 3500)
        self.assertEqual(get_votes(candidate_1, commune), 1500)

        self.assertEqual(commune.inhabitants, 9000)
        to_send = {'commune': commune_name, 'province_name': province_name, 'inhabitants': 10000,
                   'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 6000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 3500, 'candidate_1_votes': 1500}
        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertNotEqual(ret.status_code, 200)

        to_send = {'commune': commune_name, 'province_name': province_name, 'inhabitants': 10000,
                   'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 6000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 3500, 'candidate_1_votes': 2500}
        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertEqual(ret.status_code, 200)
        commune = get_commune(commune_name, get_province(province_name))
        self.assertEqual(commune.inhabitants, 10000)
        self.assertEqual(commune.valid_votes, 6000)


class GetLastModification(TestCase):
    def test_user_and_date_modification(self):
        province_name = "BB"
        commune_name = "B"
        create_province(province_name)
        comm = {'name': commune_name, 'province': get_province(province_name), 'inhabitants': 9000,
                'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                'votes': 6000, 'valid_votes': 5000}
        create_commune(comm)

        c = my_login("user_1")
        to_send = {'commune': commune_name, 'province': province_name}
        ret = c.get('/api/last_mod/', to_send, content_type="json")
        commune = get_commune(commune_name, get_province(province_name))
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(commune.last_mod_user, 'admin')

        create_candidate("Lech", "A")
        create_candidate("Donald", "B")
        commune = get_commune(commune_name, get_province(province_name))
        candidate_0 = get_candidate("Lech", "A")
        candidate_1 = get_candidate("Donald", "B")
        create_voting(candidate_0, commune, 2500)
        create_voting(candidate_1, commune, 2500)
        to_send = {'commune': commune_name, 'province_name': province_name, 'inhabitants': 9000,
                   'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                   'votes': 6000, 'valid_votes': 5000, 'candidate_0_name': 'Lech A',
                   'candidate_1_name': 'Donald B', 'candidate_0_votes': 3500, 'candidate_1_votes': 1500}
        ret = c.post('/api/update_results/', json.dumps(to_send), content_type="application/json")
        self.assertEqual(ret.status_code, 200)

        to_send = {'commune': commune_name, 'province': province_name}
        ret = c.get('/api/last_mod/', to_send, content_type="json")
        commune = get_commune(commune_name, get_province(province_name))
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(commune.last_mod_user, 'user_1')
        self.assertTrue(commune.last_mod_date >= (timezone.now() - timedelta(seconds=30)))

    def test_wrong_data(self):
        province_name = "AB"
        commune_name = "B"
        create_province(province_name)
        comm = {'name': commune_name, 'province': get_province(province_name), 'inhabitants': 9000,
                'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                'votes': 6000, 'valid_votes': 5000}
        create_commune(comm)

        c = my_login("user_1")
        to_send = {'commune': commune_name, 'province': ""}
        ret = c.get('/api/last_mod/', to_send, content_type="json")
        self.assertEqual(ret.status_code, 501)

        to_send = {'commune': "", 'province': province_name}
        ret = c.get('/api/last_mod/', to_send, content_type="json")
        self.assertEqual(ret.status_code, 501)

        to_send = {'commune': commune_name, 'province': province_name}
        ret = c.post('/api/last_mod/', json.dumps(to_send), content_type="application/json")
        self.assertEqual(ret.status_code, 405)


class GetRow(TestCase):
    def test_wrong_data(self):
        province_name = "AB"
        commune_name = "B"
        create_province(province_name)
        comm = {'name': commune_name, 'province': get_province(province_name), 'inhabitants': 9000,
                'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                'votes': 6000, 'valid_votes': 5000}
        create_commune(comm)

        c = my_login("user_1")
        to_send = {'commune_name': commune_name, 'province_name': ""}
        ret = c.get('/api/row/', to_send, content_type="json")
        self.assertEqual(ret.status_code, 501)

        to_send = {'commune_name': "", 'province_name': province_name}
        ret = c.get('/api/row/', to_send, content_type="json")
        self.assertEqual(ret.status_code, 501)

        to_send = {'commune_name': commune_name, 'province_name': province_name}
        ret = c.post('/api/row/', json.dumps(to_send), content_type="application/json")
        self.assertEqual(ret.status_code, 405)

    def test_get_row(self):
        province_name = "AB"
        commune_name = "B"
        create_province(province_name)
        comm = {'name': commune_name, 'province': get_province(province_name), 'inhabitants': 9000,
                'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                'votes': 6000, 'valid_votes': 5000}
        create_commune(comm)

        c = my_login("user_1")
        create_candidate("Lech", "A")
        create_candidate("Donald", "B")
        commune = get_commune(commune_name, get_province(province_name))
        candidate_0 = get_candidate("Lech", "A")
        candidate_1 = get_candidate("Donald", "B")
        create_voting(candidate_0, commune, 2500)
        create_voting(candidate_1, commune, 2500)
        send_post = {'commune': commune_name, 'province_name': province_name, 'inhabitants': 9000,
                     'entitled_inhabitants': 8000, 'distributed_ballots': 7000,
                     'votes': 6000, 'valid_votes': 5000, 'candidate_0_name': 'Lech A',
                     'candidate_1_name': 'Donald B', 'candidate_0_votes': 3500, 'candidate_1_votes': 1500}

        send_get = {'commune_name': commune_name, 'province_name': province_name}
        response = c.get('/api/row/', send_get, content_type="json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONNotEqual(
            str(response.data[0]),
            {'candidate_0_votes': send_post['candidate_0_votes'],
             'candidate_1_votes': send_post['candidate_1_votes'],
             'commune': commune_name,
             'distributed_ballots': send_post['distributed_ballots'],
             'entitled_inhabitants': send_post['entitled_inhabitants'],
             'inhabitants': send_post['inhabitants'],
             'province_name': province_name,
             'votes': send_post['votes'],
             'valid_votes': send_post['valid_votes']}
        )

        response = c.post('/api/update_results/', json.dumps(send_post), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        send_get = {'commune_name': commune_name, 'province_name': province_name}
        response = c.get('/api/row/', send_get, content_type="json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.data[0]),
            {'candidate_0_votes': send_post['candidate_0_votes'],
             'candidate_1_votes': send_post['candidate_1_votes'],
             'commune': commune_name,
             'distributed_ballots': send_post['distributed_ballots'],
             'entitled_inhabitants': send_post['entitled_inhabitants'],
             'inhabitants': send_post['inhabitants'],
             'province_name': province_name,
             'votes': send_post['votes'],
             'valid_votes': send_post['valid_votes']}
        )


class SeleniumModalTest(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(SeleniumModalTest, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumModalTest, self).tearDown()

    def login(self, selenium, u, p):
        selenium.get('http://127.0.0.1:8000/')
        selenium.find_element_by_id('login_link').click()
        username = selenium.find_element_by_id('username')
        password = selenium.find_element_by_id('password')
        username.send_keys(u)
        password.send_keys(p)
        selenium.find_element_by_id('submit').click()

    def test_modification_of_to_users(self):
        selenium1 = self.selenium
        self.login(selenium1, 'mati2', 'm12345678')
        self.assertEqual(selenium1.find_element_by_id('username').text, 'mati2')

        selenium2 = webdriver.Firefox()
        self.login(selenium2, 'mati', 'm12345678')
        self.assertEqual(selenium2.find_element_by_id('username').text, 'mati')

        selenium2.quit()



