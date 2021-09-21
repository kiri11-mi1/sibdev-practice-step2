import pytest
from rest_framework.test import APIClient, RequestsClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture для тестирования методов API, которые не требуют авторизацию.
 
    Returns:
        APIClient
    """
    return APIClient()
 
 
@pytest.fixture
def api_client_with_user(auth_data: dict) -> APIClient:
    """
    Fixture для тестирования методов API, которые требуют авторизацию.
 
    Parameters:
        auth_data: словарь с учетными данными
 
    Returns:
        ApiClient с пользователем
    """
    client = APIClient()
    user = User(**auth_data)
    user.set_password(auth_data.get('password', '1'))
    user.save()
    client.force_authenticate(user, RefreshToken.for_user(user).access_token)
 
    return client


@pytest.fixture
def request_client() -> RequestsClient:
    return RequestsClient()
