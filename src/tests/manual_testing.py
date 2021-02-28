from pprint import pprint
from unittest import TestCase
import pytest
import requests





BASE = 'http://127.0.0.1:5000/'
data = [{'finished': False, 'name': 'Code Notes', 'contents': 'Coding is hard but consistency and documentation helps'},
        {'finished': True, 'name': 'Swole Notes', 'contents': 'Gains are easy but like code take consistency'},
        {'finished': False, 'name': 'MLG Notes', 'contents': 'games take consistency and map knowledge to master'}]

for i in range(len(data)):
    print(BASE + 'notes/')
    response = requests.post(BASE + 'notes', json=data[i])  # make end points plural
    pprint(response.json())  # defining .json means it will be readable

input()


datas = [{'front': 'What is a calorie?', 'back': 'a unit of heat'},
        {'front': '45lb = ', 'back': '20.1kg'},
        {'front': 'How many muscles in your quads?', 'back': 'Four'}]

for i in range(len(datas)):
    print(BASE + 'flashcards/')
    response = requests.post(BASE + 'flashcards', json=datas[i])  # make end points plural
    pprint(response.json())  # defining .json means it will be readable
