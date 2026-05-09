import pytest
from django.test import TestCase
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_book_list(api_client):
    response = api_client.post('/api/books/post', {
        'title': 'Book Title',
        'author': 'Max',
        'price': 34.0,
    }, format='json')

    response = api_client.get('/api/books/')

    assert response.status_code == 200
    assert response.data == [{'title': 'Book Title', 'author': 'Max', 'price': 34.0}]


@pytest.mark.django_db
def test_book_list_empty(api_client):
    response = api_client.get('/api/books/')

    assert response.status_code == 200
    assert response.data == []


