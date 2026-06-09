from fastapi.testclient import TestClient
from app.main import app
from faker import Faker
from pytest import fixture
import asyncio

client = TestClient(app)

fake = Faker('pt_BR')
email = fake.email()
nome = fake.name()
name_film = 'Inception'

@fixture
def register():
    data = {'username': nome, 'email': email, 'password': 'test1234'}
    response = client.post('/auth/register', json=data)

@fixture
def token(register):
    form_data = {'username': nome, 'password': 'test1234'}    
    response = client.post('/auth/login', data=form_data)
    return response.json()['access_token']

@fixture
def head(token):
    return {'Authorization': f'Bearer {token}'}

@fixture
def id_film(head):
    response = client.get(f'/films/search_film/{name_film}', headers=head)
    return response.json()[0]['id']
    



def test_health():
    response =  client.get('/health') 
    assert response.json() == {"status": "ok"}
    
    
def test_register():
    data = {'username': nome, 'email': email, 'password': 'test1234'}
    response = client.post('/auth/register', json=data)
    assert response.status_code in [200, 400]


def test_login():
    form_data = {'username': nome, 'password': 'teste1234'}
    response = client.post('/auth/login', data=form_data)
    assert response.status_code in [200, 400]






def test_get_film(head):
    response = client.get(f'/films/search_film/{name_film}', headers=head)
    assert response.status_code in [200, 400]
    assert isinstance(response.json(), list)


def test_get_score(head, id_film):
    response = client.get(f'/films/get_score/{id_film}', headers=head)
    assert response.status_code in [200, 400]
    assert isinstance(response.json(), dict)





def test_post_favorite(head, id_film):
    response = client.post(f'/films/favorites/post_film', params={'movie_id': id_film}, headers=head)
    assert response.status_code == 200
    assert 'message' in response.json()

def test_get_favorites(head):
    response = client.get('/films/favorites/get_all', headers=head)
    response.status_code in [200, 400]
    assert isinstance(response.json(), list)

def test_del_favorite(head, id_film):
    response = client.delete(f'/films/favorites/del_fav', params={'id': id_film}, headers=head)
    assert response.status_code in [200, 400]


def test_websockets_querys(token):
    with client.websocket_connect(f'/ws?token={token}') as ws:
        ws.send_text('/positives')
        data = ws.receive_text()
        assert data is not None

def test_websockets_gemini(token):
    with client.websocket_connect(f'/ws?token={token}') as ws:
        ws.send_text('oi me indica um filme')
        data = ws.receive_text()
        assert data is not None