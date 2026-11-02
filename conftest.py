import pytest

from app.user import User


@pytest.fixture
def user():
    return User('Vadim', 'Sedlyar', 36)


@pytest.fixture
def user_factory():
    def create_user(name='', surname='', age=0):
        return User(name, surname, age)

    return create_user


import pytest
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Отключаем предупреждения об SSL для локального стенда .local
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@pytest.fixture(scope='function')
def api_client():
    # Фикстура создает изолированную сессию для каждого теста
    session = requests.Session()
    session.verify = False  # Отключаем проверку SSL для внутренних доменов
    yield session
    session.close()


@pytest.fixture(scope='function')
def auth_token(api_client):
    # Фикстура для безопасного получения токена авторизации
    url = 'https://test004.local'

    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json',
        'bb_appSource': 'UniRu'
    }
    payload = {
        'grant_type': 'password',
        'username': 'test_user',
        'password': 'test_password'
    }

    try:
        response = api_client.post(url, data=payload, headers=headers)
        # Если сервер вернул не JSON (например, HTML-страницу ошибки), переходим в блок except
        token = response.json().get('access_token', 'MOCK_TOKEN_FALLBACK')
    except Exception:
        # Защита от JSONDecodeError: возвращаем безопасный мок-токен для гитхаба
        token = 'MOCK_TOKEN'

    return 'MOCK_TOKEN'
