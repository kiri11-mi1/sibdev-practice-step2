import pytest
from apps.budget.models import Category
from apps.users.models import User
from django.urls import reverse
from requests.auth import HTTPBasicAuth


pytestmark = [pytest.mark.django_db]

AUTH_DATA = [{'email': 'test@mail.ru', 'username': 'test', 'password': 'qwerty'}]
PAYLOAD = {
	"name": "test",
	"type": 0,
	"owner": None
}


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_delete_owner(api_client_with_user):
    test_category = Category.objects.create(
        name="test", 
        type=0, 
        owner=api_client_with_user.handler._force_user
    )
    temp_url = reverse('api:budget:category-detail', args=(test_category.id,))

    delete_response = api_client_with_user.delete(temp_url)

    assert delete_response.status_code == 204
    assert Category.objects.all().count() == 0


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_delete_not_owner(api_client_with_user):
    test_user = User.objects.create(email='testt@mail.ru')
    test_category = Category.objects.create(name="test", type=0, owner=test_user)
    temp_url = reverse('api:budget:category-detail', args=(test_category.id,))

    delete_response = api_client_with_user.delete(temp_url)

    assert delete_response.status_code == 403
    assert Category.objects.all().count() == 1


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_get_all_auth_user(api_client_with_user):
    all_categories_url = reverse('api:budget:category-list')
    all_categories_response = api_client_with_user.get(all_categories_url)
    assert all_categories_response.status_code == 200


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_get_global_auth_user(api_client_with_user):
    global_url = reverse('api:budget:category-get-all-categories-info')
    global_response = api_client_with_user.get(global_url)
    assert global_response.status_code == 200


def test_category_get_all_anon_user(api_client):
    all_categories_url = reverse('api:budget:category-list')
    global_response = api_client.get(all_categories_url)
    assert global_response.status_code == 401


def test_category_get_global_anon_user(api_client):
    global_url = reverse('api:budget:category-get-all-categories-info')
    global_response = api_client.get(global_url)
    assert global_response.status_code == 401


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_create_with_bearer(api_client_with_user):
    category_url = reverse('api:budget:category-list')
    PAYLOAD['owner'] = api_client_with_user.handler._force_user.id
    response = api_client_with_user.post(category_url, data=PAYLOAD)
    assert response.status_code == 201

