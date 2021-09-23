import pytest
from django.urls import reverse
from rest_framework import status

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

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Category.objects.all().count() == 0


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_delete_not_owner(api_client_with_user):
    """Удаление категориии НЕ владельцем"""
    category["owner"] = User.objects.create(email='testt@mail.ru')
    tmp_category = Category.objects.create(**category)

    temp_url = reverse('api:budget:category-detail', args=(tmp_category.id,))
    response = api_client_with_user.delete(temp_url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Category.objects.all().count() == 1


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_get_all_auth_user(api_client_with_user):
    """Получение всех категорий авторизованным пользователем"""
    tmp_url = reverse('api:budget:category-list')
    response = api_client_with_user.get(tmp_url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_get_summary_auth_user(api_client_with_user):
    """Получение суммы транзакций по категориям авторизованным пользователем"""
    tmp_url = reverse('api:budget:category-get-all-categories-info')
    response = api_client_with_user.get(tmp_url)

    assert response.status_code == status.HTTP_200_OK


def test_category_get_all_anon_user(api_client):
    """Получение всех категорий НЕ авторизованным пользователем"""
    tmp_url = reverse('api:budget:category-list')
    response = api_client.get(tmp_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_category_get_summary_anon_user(api_client):
    """Получение суммы транзакций по категориям НЕ авторизованным пользователем"""
    tmp_url = reverse('api:budget:category-get-all-categories-info')
    response = api_client.get(tmp_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_category_create_by_anon_user(api_client):
    """Создание категории не авторизованным пользователем"""
    user = User.objects.create(**AUTH_DATA[0])
    category["owner"] = user.id

    tmp_url = reverse('api:budget:category-list')
    response = api_client.post(tmp_url, json=category)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Category.objects.all().count() == 0


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_category_create_by_auth_user(api_client_with_user):
    """Создание категории авторизованным пользователем"""
    category["owner"] = api_client_with_user.handler._force_user.id

    tmp_url = reverse('api:budget:category-list')
    response = api_client_with_user.post(tmp_url, data=category)

    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.all().count() == 1
