from unittest import TestCase
from base64 import b64encode
import unittest
import sqlalchemy
import bcrypt

from main import app, s
from TablesSQL import engine
import json

app.testing = True
client = app.test_client()


class BaseTestCase(TestCase):
    client = app.test_client()

    def setUp(self):
        super().setUp()

        self.user = {
            "UserId": "3",
            "Username": "Admin1",
            "Name": "Alex",
            "Surname": "John",
            "Email": "lalka",
            "Role": "User",
            "Password": "qwerty"
        }

        self.user_wrong = {
            "UserId": "3",
            "Username": "Admin1"

        }

        self.reservation = {
            "ReservationId": 4,
            "BeginTime": "2022-10-01 10:30",
            "EndTime": "2022-10-01 15:30",
            "UserId": 1,
            "RoomId": 5
        }

        self.wrong_reservation = {
            "ReservationId": 1,
            "BeginTime": "2022-10-01 20:30",
            "EndTime": "2022-10-01 15:30",
            "UserId": 0,
            "RoomId": 1
        }

        self.wrong_reservation1 = {

            "UserId": 0,
            "RoomId": 1
        }

        self.update_reservation_wrong = {
            "RoomId": 1
        }

        self.update_reservation = {
            "BeginTime": "2022-10-01 10:30",
            "EndTime": "2022-10-01 15:30",
            "UserId": 1,
            "RoomId": 1
        }

        self.admin_data_hashed = {
            "password": bcrypt.hashpw(bytes("test", 'utf-8'), bcrypt.gensalt())
        }

        #def get_auth_headers(self, credentials):
        #    return {"Authorization": f"Basic {credentials}"}

        self.admin_credentials = b64encode(b"Test:test").decode('utf-8')
        self.admin_credentials_false = b64encode(b"Test:st").decode('utf-8')

    def tearDown(self):
        self.close_session()

    def close_session(self):
        s.close()

    #def create_app(self):
    #    app.config['TESTING'] = True
    #    return app

    def get_auth_headers(self, credentials):
        return {"Authorization": f"Basic {credentials}"}


class Test(BaseTestCase):

    def test_get_user_by_id(self):
        response = self.client.get('/user/2', headers=self.get_auth_headers(self.admin_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id_wrong(self):
        response = self.client.get('/user/2', headers=self.get_auth_headers(self.admin_credentials_false))
        self.assertEqual(response.status_code, 401)

    def test_register(self):
        response = self.client.post('/user/register', json=self.user)
        self.assertEqual(response.status_code, 200)

    def test_register_wrong(self):
        response = self.client.post('/user/register', json=self.user_wrong)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        response = self.client.delete('/user/11', headers=self.get_auth_headers(self.admin_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_user_wrong(self):
        response = self.client.delete('/user/1', headers=self.get_auth_headers(self.admin_credentials))
        self.assertEqual(response.status_code, 403)

    def test_create_reservation(self):
        response = self.client.post('/reservation/create', json=self.reservation, headers=self.get_auth_headers(self.admin_credentials))
        self.assertEqual(response.status_code, 200)

    def test_wrong_create_reservation(self):
        response = self.client.post('/reservation/create', json=self.wrong_reservation, headers=self.get_auth_headers(self.admin_credentials))
        self.assertEqual(response.status_code, 200)

    def test_wrong1_create_reservation(self):
        response = self.client.post('/reservation/create', json=self.wrong_reservation1, headers=self.get_auth_headers(self.admin_credentials))
        self.assertEqual(response.status_code, 200)

 #   def test_wrong2_create_reservation(self):
 #       response = self.client.post('/reservation/create', json=self.wrong_reservation2, headers=self.get_auth_headers(self.admin_credentials))
 #       self.assertEqual(response.status_code, 200)

    def test_get_all_rooms(self):
        response = self.client.get('/reservation/rooms')

        self.assertEqual(response.status_code, 200)

    def test_get_available_room(self):
        response = self.client.get('/reservation/get/2022-10-27 15:30/2022-10-27 15:30/2')

        self.assertEqual(response.status_code, 200)

    def test_update_reservation(self):
        response = self.client.put('/reservation/rooms/5', json=self.update_reservation, headers=self.get_auth_headers(self.admin_credentials))
        self.assertEqual(response.status_code, 200)

    def test_update_reservation_wrong(self):
        response = self.client.put('/reservation/rooms/5', json=self.update_reservation_wrong, headers=self.get_auth_headers(self.admin_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_reservation(self):
        response = self.client.delete('/reservation/rooms/4', json=self.update_reservation, headers=self.get_auth_headers(self.admin_credentials))
        self.assertEqual(response.status_code, 200)

