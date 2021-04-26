from pprint import pprint
from unittest import TestCase
import pytest
from ..schemas import NotesSchema, FlashCardSchema, UserSchema
from ..tests.fixtures import client, db
from unittest.mock import ANY
from ..models import UserModel

from ..resources.users import app, guard
from ..config import db, app
import tempfile
import os


class UserTestCase(TestCase):
    def setUp(self) -> None:
        db.drop_all()
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app
        self.client = app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.create_all()
        data = {'username': 'test_user1',
                'password': 'test_user1_password'}
        password = guard.hash_password('test_user1_password')
        self.test_user = UserModel(username='test_user1', password=password)
        db.session.add(self.test_user)
        db.session.commit()
        with self.client:
            response = self.client.post('/login', json=data)
            self.auth_code = response.json['access_token']
            self.auth_header = {'Authorization': f'Bearer {self.auth_code}'}
        super().setUp()

    def tearDown(self) -> None:
        db.drop_all()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        super().tearDown()


class TestSchema(TestCase):
    def test_notes_schema(self):
        data = {'contents': 'games take consistency and map knowledge to master',
                'finished': False,
                'name': 'MLG Notes'}

        result = NotesSchema().load(data)
        assert result == {'contents': 'games take consistency and map knowledge to master',
                          'finished': False,
                          'name': 'MLG Notes'}

    def test_flashcards_schema(self):
        data = {'front': 'what does a test look like?',
                'back': 'like this'}

        result = FlashCardSchema().load(data)
        assert result == {'front': 'what does a test look like?',
                          'back': 'like this'}

    def test_users_schema(self):
        data = {'username': 'test_user1',
                'password': 'test_user1_password'}

        result = UserSchema().load(data)
        assert result == {'username': 'test_user1',
                          'password': 'test_user1_password'}


class TestNotes(UserTestCase):
    # client = client()
    def test_notes_post(self):
        response = self.client.get('/notes', headers=self.auth_header)
        assert response.status_code == 200
        assert response.json == []
        data = {
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps #coding'
        }
        expected = {
            'id': ANY,
            'date_created': ANY,
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps #coding',
            'tags': ['coding']
        }
        response = self.client.post('/notes', json=data, headers=self.auth_header)
        assert response.status_code == 201
        response = self.client.get('/notes', headers=self.auth_header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0] == expected

    # def test_encode_auth_token(self, client, db):
    #     data = {'username': 'test_user1',
    #             'password': 'test_user1_password'}
    #
    #     response = client.post('/login', json=data)
    #     assert response.status_code == 201
    #
    #     db.session.add(data)
    #     db.session.commit()
    #     yield client, db
    #     auth_token = data.access_token(data.id)
    #     self.assertTrue(isinstance(auth_token, bytes))

    def test_notes_delete(self):
        response = self.client.get('/notes', headers=self.auth_header)
        assert response.status_code == 200
        assert response.json == []
        data = {
            'finished': False,
            'name': 'Code Notes',
            'contents': 'This note needs to be deleted'
        }
        response = self.client.post('/notes', json=data, headers=self.auth_header)
        assert response.status_code == 201
        response = self.client.delete('/notes/'+str(response.json['id']), headers=self.auth_header)
        assert response.status_code == 200
        response = self.client.get('/notes', headers=self.auth_header)
        assert response.status_code == 200
        assert response.json == []

    def tests_notes_get(self):
        data = {
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps #coding'
        }
        expected = {
            'id': ANY,
            'date_created': ANY,
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps #coding',
            'tags': ['coding']
        }
        response = self.client.post('/notes', json=data, headers=self.auth_header)
        assert response.status_code == 201
        response = self.client.get('/notes', headers=self.auth_header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0] == expected

    def tests_notes_completed(self):
        data = {
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps'
        }
        expected = {
            'id': ANY,
            'date_created': ANY,
            'finished': True,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps',
            'tags': []
        }
        response = self.client.post('/notes', json=data, headers=self.auth_header)
        assert response.status_code == 201
        response = self.client.put(f'/notes/{response.json["id"]}/complete', headers=self.auth_header)
        assert response.status_code == 200
        assert response.json == expected

    def tests_notes_incompleted(self):
        data = {
            'finished': True,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps'
        }
        expected = {
            'id': ANY,
            'date_created': ANY,
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps',
            'tags': []
        }
        response = self.client.post('/notes', json=data, headers=self.auth_header)
        assert response.status_code == 201
        response = self.client.put(f'/notes/{response.json["id"]}/incomplete', headers=self.auth_header)
        assert response.status_code == 200
        assert response.json == expected


class TestFlashCards(UserTestCase):

    def test_flashcard_post(self):
        response = self.client.get('/flashcards', headers=self.auth_header)
        assert response.status_code == 200
        assert response.json == []
        data = {'front': 'what does a test look like?',
                'back': 'like this #test'}
        expected = {
            'id': ANY,
            'date_created': ANY,
            'date_due': ANY,
            'front': 'what does a test look like?',
            'back': 'like this #test',
            'tags': ['test']
        }
        response = self.client.post('/flashcards', json=data, headers=self.auth_header)
        assert response.status_code == 201
        response = self.client.get('/flashcards', headers=self.auth_header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0] == expected

    def test_flashcards_delete(self):
        response = self.client.get('/flashcards', headers=self.auth_header)
        assert response.status_code == 200
        assert response.json == []
        data = {'front': 'what does a test look like?',
                'back': 'like this'}
        response = self.client.post('/flashcards', json=data, headers=self.auth_header)
        assert response.status_code == 201
        response = self.client.delete('/flashcards/'+str(response.json['id']), headers=self.auth_header)
        assert response.status_code == 200
        response = self.client.get('/flashcards', headers=self.auth_header)
        assert response.status_code == 200
        assert response.json == []

    def tests_flashcards_get(self):
        data = {'front': 'what does a test look like?',
                'back': 'like this'}
        expected = {
            'id': ANY,
            'date_created': ANY,
            'date_due': ANY,
            'front': 'what does a test look like?',
            'back': 'like this',
            'tags': []
        }
        response = self.client.post('/flashcards', json=data, headers=self.auth_header)
        assert response.status_code == 201
        response = self.client.get('/flashcards', headers=self.auth_header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0] == expected


class TestSummaries(UserTestCase):

    def tests_summaries_get(self):
        text_summer_data = {'finished': False, 'name': 'Code Notes',
                             'contents': 'A computer is a machine that can be instructed to carry out sequences of arithmetic or logical operations automatically via computer programming. Modern computers have the ability to follow generalized sets of operations, called programs. These programs enable computers to perform an extremely wide range of tasks. A "complete" computer including the hardware, the operating system (main software), and peripheral equipment required and used for "full" operation can be referred to as a computer system. This term may as well be used for a group of computers that are connected and work together, in particular a computer network or computer cluster.'}
        response = self.client.post('/notes', json=text_summer_data, headers=self.auth_header)
        response2 = self.client.get(f'/note-summaries/{response.json["id"]}', json=text_summer_data, headers=self.auth_header)
        pass


# class TestUsers:
#
#     @pytest.mark.usefixtures('client')
#     def test_users_post(self, client):
#         response = client.get('/users')
#         assert response.status_code == 200
#         assert response.json == []
#         data = {'username': 'test_user1',
#                 'password_hash': 'test_user1_password'}
#         expected = {
#             'id': ANY,
#             'username': 'test_user1'
#         }
#         response = client.post('/users', json=data)
#         assert response.status_code == 201
#         response = client.get('/users')
#         assert response.status_code == 200
#         assert len(response.json) == 1
#         assert response.json[0] == expected
#
#


# # pytest - assert condition == value e.g. run data + first loop. assert responce.jason() == data?
# BASE = 'http://127.0.0.1:5000/'
# data = [{'finished': False, 'name': 'Code Notes', 'contents': 'Coding is hard but consistency and documentation helps'},
#         {'finished': True, 'name': 'Swole Notes', 'contents': 'Gains are easy but like code take consistency'},
#         {'finished': False, 'name': 'MLG Notes', 'contents': 'games take consistency and map knowledge to master'}]
#
# for i in range(len(data)):
#     print(BASE + 'note/')
#     responce = requests.post(BASE + 'note', json=data[i])  # make end points plural
#     pprint(responce.json())  # defining .json means it will be readable
#
# input()
#
# x = requests.get(BASE + 'note')
# pprint(x.json())
# # input()


# # 'delete method'
# responce = requests.delete(BASE + 'note/3')
# pprint(responce.json())  # defining .json means it will be readable

# input()
# x = requests.get(BASE + 'note')
#
# pprint(x.json())

# responce = requests.get(BASE + 'video/') #q for paddy, how to return all with get
# print(responce.json())

# #
# input()
# # # import pdb; pdb.set_trace()
# responce = requests.patch(BASE + 'note/2', json={'contents': 'This note has been patched!'})
# #
# pprint(responce.json())  # defining .json means it will be readable
#
# # x = requests.get(BASE + 'note')
# pprint(x.json())

# views = contents
# likes = finished bool
