from fastapi.testclient import TestClient
from app.main import app
from faker import Faker
from pytest import fixture
import random

client = TestClient(app)

fake = Faker('pt_BR')
email = fake.email()
nome = fake.name()
name_film = 'Inception'


@fixture
def token():
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
    

# @fixture
# def id_user():    
#     form_data = {'username': nome, 'password': 'teste1234'}
#     response = client.post('/login', data=form_data)
#     return response.json()['user_id']
    
# @fixture
# def id_workout(id_user, head):
#     data = {'id_user': id_user}
#     response =  client.post(f'/workout', json=data, headers=head) 
#     return response.json()['data']['id']

# @fixture 
# def id_exercise(head):
#     response =  client.get(f'/exercises', headers=head) 
#     return response.json()[0]['id']

# @fixture
# def id_workout_exercise(id_workout, id_exercise, head):
#     data = {'id_workout': id_workout, 'id_exercise': id_exercise}
#     response =  client.post(f'/workout_exercise', json=data, headers=head) 
#     return response.json()['data']['id']

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



# def test_post_exercise(head):
#     data = {'exercise': 'Rosca martelo'}
#     response =  client.post(f'/exercises', params=data, headers=head) 
#     assert response.status_code == 200
#     assert 'message' in response.json()

# def test_post_workout(id_user, head):
#     data = {'id_user': id_user}
#     response =  client.post(f'/workout', json=data, headers=head) 
#     assert response.status_code == 200
#     assert 'id' in response.json()['data']

# def test_post_workout_exercise(id_workout, id_exercise, head):
#     data = {'id_workout': id_workout, 'id_exercise': id_exercise}
#     response =  client.post(f'/workout_exercise', json=data, headers=head) 
#     assert response.status_code == 200
#     assert  'id' in response.json()['data']

def test_post_favorite(head, id_film):
    response = client.post(f'/films/favorites/post_film/{id_film}', headers=head)
    assert response.status_code == 200
    assert 'message' in response.json()

# def test_post_sets(id_workout_exercise, head):
#     weight = random.randint(1, 50)
#     reps = random.randint(5, 12)
#     data = {'weight': weight, 'reps': reps, 'id_workout_exercise': id_workout_exercise}
#     response = client.post(f'/sets', json=data, headers=head) 
    
#     assert response.status_code == 200 
#     assert  'message' and 'pr' in response.json()


def test_get_film(head):
    response = client.get(f'/films/search_film/{name_film}', headers=head)
    assert response.status_code in [200, 400]
    assert isinstance(response.json(), list)

# def test_get_exercises(head):
#     response = client.get('/exercises', headers=head) 
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
    
# def test_get_history(head):
#     response = client.get(f'history/{nome}', headers=head)
#     assert response.status_code in [200, 400]
#     assert isinstance(response.json(), list)

def test_get_score(head, id_film):
    response = client.get(f'/films/get_score/{id_film}', headers=head)
    assert response.status_code in [200, 400]
    assert isinstance(response.json(), dict)

# def test_get_workout_detail(head, id_user):
#     response = client.get(f'workout_detail_w_user/{id_user}', headers=head)
#     assert response.status_code in [200, 400]
#     assert isinstance(response.json(), list)

# def test_logout(head):
#     response = client.post(f'/logout',  headers=head) 
#     assert response.status_code in [200, 400]