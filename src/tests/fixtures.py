import os
import tempfile
from unittest import TestCase

import pytest
from ..resources.notes import app
from ..resources.flashcards import app
from ..resources.users import app
from ..config import db


@pytest.fixture
def client():

    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            # test_user = UserModel(username='test_user1', password='test_user1_password')
            # db.session.add(test_user)
            # db.session.commit()
        yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])
