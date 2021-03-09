from pprint import pprint
from unittest import TestCase
import pytest

from schemas import NotesSchema, FlashCardSchema
from tests.fixtures import client
from unittest.mock import ANY


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


class TestNotes:
    # client = client()
    @pytest.mark.usefixtures('client')
    def test_notes_post(self, client):
        response = client.get('/notes')
        assert response.status_code == 200
        assert response.json == []
        data = {
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps'
        }
        expected = {
            'id': ANY,
            'date_created': ANY,
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps'
        }
        response = client.post('/notes', json=data)
        assert response.status_code == 201
        response = client.get('/notes')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0] == expected

    def test_notes_delete(self, client):
        response = client.get('/notes')
        assert response.status_code == 200
        assert response.json == []
        data = {
            'finished': False,
            'name': 'Code Notes',
            'contents': 'This note needs to be deleted'
        }
        response = client.post('/notes', json=data)
        assert response.status_code == 201
        response = client.delete('/notes/'+str(response.json['id']))
        assert response.status_code == 200
        response = client.get('/notes')
        assert response.status_code == 200
        assert response.json == []

    def tests_notes_get(self, client):
        data = {
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps'
        }
        expected = {
            'id': ANY,
            'date_created': ANY,
            'finished': False,
            'name': 'Code Notes',
            'contents': 'Coding is hard but consistency and documentation helps'
        }
        response = client.post('/notes', json=data)
        assert response.status_code == 201
        response = client.get('/notes')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0] == expected


class TestFlashCards:

    @pytest.mark.usefixtures('client')
    def test_flashcard_post(self, client):
        response = client.get('/flashcards')
        assert response.status_code == 200
        assert response.json == []
        data = {'front': 'what does a test look like?',
                'back': 'like this'}
        expected = {
            'id': ANY,
            'date_created': ANY,
            'date_viewed': ANY,
            'front': 'what does a test look like?',
            'back': 'like this'
        }
        response = client.post('/flashcards', json=data)
        assert response.status_code == 201
        response = client.get('/flashcards')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0] == expected

    def test_flashcards_delete(self, client):
        response = client.get('/flashcards')
        assert response.status_code == 200
        assert response.json == []
        data = {'front': 'what does a test look like?',
                'back': 'like this'}
        response = client.post('/flashcards', json=data)
        assert response.status_code == 201
        response = client.delete('/flashcards/'+str(response.json['id']))
        assert response.status_code == 200
        response = client.get('/flashcards')
        assert response.status_code == 200
        assert response.json == []

    def tests_flashcards_get(self, client):
        data = {'front': 'what does a test look like?',
                'back': 'like this'}
        expected = {
            'id': ANY,
            'date_created': ANY,
            'date_viewed': ANY,
            'front': 'what does a test look like?',
            'back': 'like this'
        }
        response = client.post('/flashcards', json=data)
        assert response.status_code == 201
        response = client.get('/flashcards')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0] == expected


class TestSummaries:


    @pytest.mark.usefixtures('client')
    def tests_summaries_get(self, client):
        text_summer_data = {'finished': False, 'name': 'Code Notes',
                             'contents': 'A computer is a machine that can be instructed to carry out sequences of arithmetic or logical operations automatically via computer programming. Modern computers have the ability to follow generalized sets of operations, called programs. These programs enable computers to perform an extremely wide range of tasks. A "complete" computer including the hardware, the operating system (main software), and peripheral equipment required and used for "full" operation can be referred to as a computer system. This term may as well be used for a group of computers that are connected and work together, in particular a computer network or computer cluster.'}
        response = client.post('/notes', json=text_summer_data)
        response2 = client.get(f'/note-summaries/{response.json["id"]}', json=text_summer_data)
        import pdb;pdb.set_trace()
        pass




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
