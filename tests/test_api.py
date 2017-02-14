import os

import json
import pytest

os.environ['TEST'] = '1'
if os.path.exists('travel_planner/test.db'):
    os.remove('travel_planner/test.db')

from travel_planner.main import app, db, api
from travel_planner.models import Trip, User
from travel_planner.api import UserView, UsersView, TripsFilterView, TripsView, TripView

api.add_resource(UsersView, '/users')
api.add_resource(UserView, '/users/<username>')
api.add_resource(TripsView, '/users/<username>/trips')
api.add_resource(TripView, '/users/<username>/trips/<int:trip_id>')
api.add_resource(TripsFilterView, '/users/<username>/trips/<from_date>&<to_date>')


@pytest.fixture(autouse=True)
def tear_up_down_db():
    db.create_all()

    yield

    db.drop_all()


app = app.test_client()

headers = {'Content-Type': 'application/json'}

def request(method, url, token=None, **kwargs):
    headers = kwargs.get('headers', {})
    if token:
        headers['Authorization'] = 'JWT ' + token

    kwargs['headers'] = headers

    return app.open(url, method=method, **kwargs)


def register_user(username, password, role="user"):
    return request('POST', '/api/users', data=json.dumps({'username': username, 'password': password, 'role': role}), headers=headers)

def create_trip(token, username):
    return request('POST', '/api/users/' + username + '/trips', token=token, data=json.dumps({
                                                                                        "destination":"dest",
                                                                                        "comment": "comm",
                                                                                        "startDate": "02/02/2015",
                                                                                        "endDate": "03/03/2015"
                                                                                    }), headers=headers)


def get_token(username, password):
    response = request('POST', '/api/token', data=json.dumps({'username': username, 'password': password}), headers=headers)

    return json.loads(response.data)["access_token"]


def test_post_users_registers_user():
    response = register_user("test", "test")

    assert "success" in response.data 


def test_get_users_gets_all_users():
    register_user("test", "test")
    token = get_token("test", "test")

    response = request('GET', '/api/users', token=token, headers=headers)

    assert 'test' in response.data


def test_update_user_updates_user():
    register_user("test", "test")
    token = get_token("test", "test")

    response = request('PUT', '/api/users/test', data=json.dumps({'username': 'test1'}), token=token, headers=headers)

    assert 'test1' in response.data


def test_delete_user_deletes_user():
    register_user("test", "test")
    token = get_token("test", "test")

    response = request('DELETE', '/api/users/test', token=token, headers=headers)

    assert 'success' in response.data


def test_admin_update_user_updates_user():
    register_user("admin", "test", role="admin")
    register_user("test", "test")

    token = get_token("admin", "test")

    response = request('PUT', '/api/users/test', data=json.dumps({'username': 'test1'}), token=token, headers=headers)

    assert 'test1' in response.data


def test_user_manager_update_user_updates_user():
    register_user("manager", "test", role="user_manager")
    register_user("test", "test")

    token = get_token("manager", "test")

    response = request('PUT', '/api/users/test', data=json.dumps({'username': 'test1'}), token=token, headers=headers)

    assert 'test1' in response.data  


def test_other_user_update_user_cant_update_user():
    register_user("tester", "test")
    register_user("test", "test")

    token = get_token("tester", "test")

    response = request('PUT', '/api/users/test', data=json.dumps({'username': 'test1'}), token=token, headers=headers)

    assert 'error' in response.data  


def test_admin_delete_user_deletes_user():
    register_user("admin", "test", role="admin")
    register_user("test", "test")

    token = get_token("admin", "test")

    response = request('DELETE', '/api/users/test', token=token, headers=headers)

    assert 'success' in response.data


def test_user_manager_delete_user_deletes_user():
    register_user("manager", "test", role="user_manager")
    register_user("test", "test")

    token = get_token("manager", "test")

    response = request('DELETE', '/api/users/test', token=token, headers=headers)

    assert 'success' in response.data  


def test_other_user_delete_user_cant_delete_user():
    register_user("tester", "test")
    register_user("test", "test")

    token = get_token("tester", "test")

    response = request('DELETE', '/api/users/test', token=token, headers=headers)

    assert 'error' in response.data  


def test_post_trip_saves_trip():
    register_user("test", "test")
    token = get_token("test", "test")

    response = create_trip(token, "test")

    assert "success" in response.data


def test_get_user_trips_returns_right_trips():
    register_user("test", "test")
    token = get_token("test", "test")

    create_trip(token, "test")

    response = request('GET', '/api/users/test/trips', token=token, headers=headers)

    assert 'destination' in response.data


def test_put_user_trips_updates_trip():
    register_user("test", "test")
    token = get_token("test", "test")

    create_trip(token, "test")

    response = request('PUT', '/api/users/test/trips/1', token=token, data=json.dumps({"destination":"destt",
                                                                                        "comment": "comm",
                                                                                        "startDate": "02/02/2015",
                                                                                        "endDate": "03/03/2015"
                                                                                     }), headers=headers)

    assert 'destt' in response.data                                 


def test_delete_user_trips_deletes_trip():
    register_user("test", "test")
    token = get_token("test", "test")

    create_trip(token, "test")

    response = request('DELETE', '/api/users/test/trips/1', token=token, headers=headers)

    assert "success" in response.data


def test_admin_update_user_trips_updates_trip():
    register_user("admin", "test", role="admin")
    register_user("test", "test")

    admin_token = get_token("admin", "test")
    user_token = get_token("test", "test")
    
    create_trip(user_token, "test")

    response = request('PUT', '/api/users/test/trips/1', token=admin_token, data=json.dumps({
                                                                                        "destination":"destt",
                                                                                        "comment": "comm",
                                                                                        "startDate": "02/02/2015",
                                                                                        "endDate": "03/03/2015"
                                                                                     }), headers=headers)
    
    assert 'destt' in response.data


def test_admin_delete_user_trips_deletes_trip():
    register_user("admin", "test", role="admin")
    register_user("test", "test")

    admin_token = get_token("admin", "test")
    user_token = get_token("test", "test")
    
    create_trip(user_token, "test")

    response = request('DELETE', '/api/users/test/trips/1', token=admin_token, headers=headers)

    assert 'success' in response.data


def test_user_tries_to_update_other_user_trip_returns_error():
    register_user("tester", "test")
    register_user("test", "test")

    tester_token = get_token("tester", "test")
    user_token = get_token("test", "test")
    
    create_trip(user_token, "test")

    response = request('PUT', '/api/users/test/trips/1', token=tester_token, data=json.dumps({
                                                                                        "destination":"destt",
                                                                                        "comment": "comm",
                                                                                        "startDate": "02/02/2015",
                                                                                        "endDate": "03/03/2015"
                                                                                     }), headers=headers)
    
    assert 'error' in response.data


def test_user_tries_to_delete_other_user_trip_returns_error():
    register_user("tester", "test")
    register_user("test", "test")

    tester_token = get_token("tester", "test")
    user_token = get_token("test", "test")
    
    create_trip(user_token, "test")

    response = request('DELETE', '/api/users/test/trips/1', token=tester_token, headers=headers)

    assert 'error' in response.data