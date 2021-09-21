import pytest
from django.urls import reverse

from apps.budget.models import Category
from apps.users.models import User
from apps.budget.tests.mock_data import *

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_delete_owner(api_client_with_user):
    """Удаление категориии владельцем"""
    category["owner"] = api_client_with_user.handler._force_user
    tmp_category = Category.objects.create(**category)

    temp_url = reverse('api:budget:category-detail', args=(tmp_category.id,))
    response = api_client_with_user.delete(temp_url)

    assert response.status_code == 204
    assert Category.objects.all().count() == 0


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_delete_not_owner(api_client_with_user):
    """Удаление категориии НЕ владельцем"""
    category["owner"] = User.objects.create(email='testt@mail.ru')
    tmp_category = Category.objects.create(**category)

    temp_url = reverse('api:budget:category-detail', args=(tmp_category.id,))
    response = api_client_with_user.delete(temp_url)

    assert response.status_code == 403
    assert Category.objects.all().count() == 1


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_get_all_auth_user(api_client_with_user):
    """Получение всех категорий авторизованным пользователем"""
    tmp_url = reverse('api:budget:category-list')
    response = api_client_with_user.get(tmp_url)

    assert response.status_code == 200


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_get_global_auth_user(api_client_with_user):
    """Получение блока Global авторизованным пользователем"""
    tmp_url = reverse('api:budget:category-get-all-categories-info')
    response = api_client_with_user.get(tmp_url)

    assert response.status_code == 200


def test_category_get_all_anon_user(api_client):
    """Получение всех категорий НЕ авторизованным пользователем"""
    tmp_url = reverse('api:budget:category-list')
    response = api_client.get(tmp_url)

    assert response.status_code == 401


def test_category_get_global_anon_user(api_client):
    """Получение блока Global НЕ авторизованным пользователем"""
    tmp_url = reverse('api:budget:category-get-all-categories-info')
    response = api_client.get(tmp_url)

    assert response.status_code == 401


def test_category_create_with_basic_auth(request_client):
    """Создание категории с Basic токеном"""
    user = User.objects.create(**AUTH_DATA[0])
    category_payload["owner"] = user.id

    tmp_url = "http://testserver" + reverse('api:budget:category-list')
    response = request_client.post(
        tmp_url,
        json=category_payload,
        headers={'Authorization': 'Basic cbaghvscghsa'}
    )

    assert response.status_code == 401


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_create_with_bearer(api_client_with_user):
    """Создание категории с Bearer токеном"""
    category_payload["owner"] = api_client_with_user.handler._force_user.id

    tmp_url = reverse('api:budget:category-list')
    response = api_client_with_user.post(tmp_url, data=category_payload)

    assert response.status_code == 201
