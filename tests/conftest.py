import pytest
from django.contrib.auth.models import User

HOME_URL = "/"
LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"


@pytest.fixture
def client():
    from django.test.client import Client
    return Client()


@pytest.fixture(scope='package')
def base_users():
    return User.objects.all().order_by('id')


@pytest.mark.django_db
def get_tested_url_for_max_id(url_pattern, Model):
    url_begin, url_end = url_pattern.split('<pk>')
    max_id = Model.objects.latest('id').id
    full_url = url_begin + str(max_id) + url_end
    return full_url
