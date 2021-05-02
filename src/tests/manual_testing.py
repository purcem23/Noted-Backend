from pprint import pprint
from unittest import TestCase
import pytest
import requests

user_data = {"front": "Admin User", "back": "test101"}
BASE = "http://127.0.0.1:5000/"
data = [
    {
        "finished": False,
        "name": "Code Notes",
        "contents": "Coding is hard but consistency and documentation helps",
    },
    {
        "finished": True,
        "name": "Swole Notes",
        "contents": "Gains are easy but like code take consistency",
    },
    {
        "finished": False,
        "name": "MLG Notes",
        "contents": "games take consistency and map knowledge to master",
    },
]

# text_summer_data = [{'finished': False, 'name': 'Code Notes',
#                      'contents': 'A computer is a machine that can be instructed to carry out sequences of arithmetic or logical operations automatically via computer programming. Modern computers have the ability to follow generalized sets of operations, called programs. These programs enable computers to perform an extremely wide range of tasks. A "complete" computer including the hardware, the operating system (main software), and peripheral equipment required and used for "full" operation can be referred to as a computer system. This term may as well be used for a group of computers that are connected and work together, in particular a computer network or computer cluster.'}]
#
# for i in range(len(text_summer_data)):
#     print(BASE + 'notes/')
#     response = requests.post(BASE + 'notes', json=text_summer_data[i])  # make end points plural
#     print(response.json())  # defining .json means it will be readable

#
# for i in range(len(data)):
#     print(BASE + 'notes/')
#     response = requests.post(BASE + 'notes', json=data[i])  # make end points plural
#     print(response.json())  # defining .json means it will be readable
#

for i in range(len(user_data)):
    print(BASE + "flashcards/")
    response = requests.post(
        BASE + "flashcards", json=user_data
    )  # make end points plural
    print(response.json())  # defining .json means it will be readable


# input()
# x = requests.get(BASE + 'notes')
# pprint(x.json())
# # input()


# datas = [{'front': 'What is a calorie?', 'back': 'a unit of heat'},
#         {'front': '45lb = ', 'back': '20.1kg'},
#         {'front': 'How many muscles in your quads?', 'back': 'Four'}]
#
# for i in range(len(datas)):
#     print(BASE + 'flashcards/')
#     response = requests.post(BASE + 'flashcards', json=datas[i])  # make end points plural
#     pprint(response.json())  # defining .json means it will be readable
