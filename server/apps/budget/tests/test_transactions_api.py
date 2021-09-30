import pytest
from django.urls import reverse
from rest_framework import status
from datetime import datetime
from random import randint as rd

from apps.budget.models import Transaction, Category
from apps.users.models import User
from apps.budget.tests.mock_data import *

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_transaction_delete_owner(api_client_with_user):
    """Удаление категориии владельцем"""
    category["owner"] = api_client_with_user.handler._force_user
    transaction["owner"] = api_client_with_user.handler._force_user
    transaction["category"] = Category.objects.create(**category)
    tmp_transaction = Transaction.objects.create(**transaction)

    temp_url = reverse('api:budget:transaction-detail', args=(tmp_transaction.id,))
    response = api_client_with_user.delete(temp_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Transaction.objects.all().count() == 0


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_transaction_delete_not_owner(api_client_with_user):
    """Удаление категориии НЕ владельцем"""
    user = User.objects.create(email='testt@mail.ru')
    category["owner"], transaction["owner"]  = user, user
    transaction["category"] = Category.objects.create(**category)
    tmp_transaction = Transaction.objects.create(**transaction)

    temp_url = reverse('api:budget:transaction-detail', args=(tmp_transaction.id,))
    response = api_client_with_user.delete(temp_url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Transaction.objects.all().count() == 1


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_transaction_global_by_auth_user(api_client_with_user):
    """Получения доходов и расходов авторизованным пользователем"""
    tmp_url = reverse('api:budget:transaction-global-info')
    response = api_client_with_user.get(tmp_url)

    assert response.status_code == status.HTTP_200_OK


def test_transaction_global_by_anon_user(api_client):
    """Получения доходов и расходов авторизованным пользователем"""
    tmp_url = reverse('api:budget:transaction-global-info')
    response = api_client.get(tmp_url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_transaction_create_by_anon_user(api_client):
    """Создание транзакции не авторизованным пользователем"""
    user = User.objects.create(**AUTH_DATA[0])
    category["owner"], transaction["owner"]  = user, user.id
    transaction["category"] = Category.objects.create(**category).id

    tmp_url = reverse('api:budget:transaction-list')
    response = api_client.post(tmp_url, json=transaction)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Transaction.objects.all().count() == 0


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_transaction_create_by_auth_user(api_client_with_user):
    """Создание транзакции авторизованным пользователем"""
    user = api_client_with_user.handler._force_user
    category["owner"], transaction["owner"] = user, user.id
    transaction["category"] = Category.objects.create(**category).id

    tmp_url = reverse('api:budget:transaction-list')
    response = api_client_with_user.post(tmp_url, data=transaction)

    assert response.status_code == status.HTTP_201_CREATED
    assert Transaction.objects.all().count() == 1


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_transaction_create_by_auth_user(api_client_with_user):
    """Создание транзакции авторизованным пользователем"""
    user = api_client_with_user.handler._force_user
    category["owner"], transaction["owner"] = user, user.id
    transaction["category"] = Category.objects.create(**category).id

    tmp_url = reverse('api:budget:transaction-list')
    response = api_client_with_user.post(tmp_url, data=transaction)

    assert response.status_code == status.HTTP_201_CREATED
    assert Transaction.objects.all().count() == 1


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_transaction_put_by_auth_user(api_client_with_user):
    """Изменение транзакции методом PUT авторизованным пользователем"""
    user = api_client_with_user.handler._force_user

    category["owner"] = user
    tmp_category = Category.objects.create(**category)

    transaction.update({"category": tmp_category, "owner": user})
    tmp_transaction = Transaction.objects.create(**transaction)

    transaction.update({
        "category": tmp_category.id,
        "owner": user.id,
        "amount": rd(1, 15000)
    })

    expected = {
        "id": tmp_transaction.id,
        "owner": user.id,
        "amount": f'{transaction["amount"]:.2f}',
        "date": str(datetime.now().strftime('%Y-%m-%d')),
        "category": tmp_category.id,
        "category_type": tmp_category.type
    }

    tmp_url = reverse('api:budget:transaction-detail', args=(tmp_transaction.id,))
    response = api_client_with_user.put(tmp_url, data=transaction)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected


def test_transaction_put_by_anon_user(api_client):
    user = User.objects.create(**AUTH_DATA[0])

    category["owner"] = user
    tmp_category = Category.objects.create(**category)

    transaction.update({"category": tmp_category, "owner": user})
    tmp_transaction = Transaction.objects.create(**transaction)

    tmp_url = reverse('api:budget:transaction-detail', args=(tmp_transaction.id,))
    response = api_client.put(tmp_url, data=transaction)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
