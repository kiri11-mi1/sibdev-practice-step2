import pytest
from django.urls import reverse

from apps.budget.models import Category, Widget
from apps.users.models import User
from apps.budget.tests.mock_data import *

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_widget_delete_owner(api_client_with_user):
    """Удаление виджета владельцем"""
    category["owner"] = api_client_with_user.handler._force_user
    widget["owner"] = api_client_with_user.handler._force_user
    widget["category"] = Category.objects.create(**category)
    tmp_widget = Widget.objects.create(**widget)

    temp_url = reverse('api:budget:widget-detail', args=(tmp_widget.id,))
    response = api_client_with_user.delete(temp_url)

    assert response.status_code == 204
    assert Widget.objects.all().count() == 0


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_widget_delete_not_owner(api_client_with_user):
    """Удаление виджета НЕ владельцем"""
    tmp_user = User.objects.create(email='testt@mail.ru')
    category["owner"] = tmp_user
    widget["owner"] = tmp_user
    widget["category"] = Category.objects.create(**category)
    tmp_widget = Widget.objects.create(**widget)

    temp_url = reverse('api:budget:widget-detail', args=(tmp_widget.id,))
    response = api_client_with_user.delete(temp_url)

    assert response.status_code == 403
    assert Widget.objects.all().count() == 1


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_widget_get_all_auth_user(api_client_with_user):
    tmp_url = reverse('api:budget:widget-list')
    response = api_client_with_user.get(tmp_url)

    assert response.status_code == 200


def test_widget_get_all_anon_user(api_client):
    tmp_url = reverse('api:budget:widget-list')
    response = api_client.get(tmp_url)

    assert response.status_code == 401


@pytest.mark.parametrize('auth_data', AUTH_DATA)
def test_widget_create_with_bearer(api_client_with_user):
    widget_payload["owner"] = api_client_with_user.handler._force_user.id
    category["owner"] = api_client_with_user.handler._force_user
    widget_payload["category"] = Category.objects.create(**category).id

    tmp_url = reverse('api:budget:widget-list')
    response = api_client_with_user.post(tmp_url, data=widget_payload)

    assert response.status_code == 201
