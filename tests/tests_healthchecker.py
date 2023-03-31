from unittest.mock import patch

from fastapi import status

from src.services.messages_templates import WELCOME_MESSAGE
from src.services.urls_templates import URL_TO_HEALTHCHECKER


def test_healthchecker_successful(client, session):
    with patch('main.get_db', return_value=session):
        response = client.get(URL_TO_HEALTHCHECKER)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": WELCOME_MESSAGE}
