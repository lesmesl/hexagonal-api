# poetry run python scripts/test_user_use_case.py

import os
import sys

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import MagicMock

from fastapi import HTTPException

from app.users.application.use_cases import UserUseCase
from app.users.infrastructure.dtos import UserResponseSchema
from app.users.infrastructure.repository import UserRepository


class TestUserUseCase(unittest.TestCase):
    def setUp(self):
        self.user_repository = MagicMock(spec=UserRepository)
        self.use_case = UserUseCase(self.user_repository)
        self.valid_token = "valid_token"
        self.invalid_token = "invalid_token"
        self.user = UserResponseSchema(id=1, email="user@example.com", username="user")
        # self.user_error = {id=1, email="user", username="user"}

    def test_get_current_user_v1_valid_token(self):
        self.user_repository.get_current_user.return_value = self.user
        result = self.use_case.get_current_user_v1(self.valid_token)
        self.assertEqual(result, self.user)
        self.user_repository.get_current_user.assert_called_once_with(self.valid_token)

    def test_get_current_user_v1_invalid_token(self):
        self.user_repository.get_current_user.side_effect = HTTPException(
            status_code=401, detail="Invalid token"
        )
        with self.assertRaises(HTTPException):
            self.use_case.get_current_user_v1(self.invalid_token)
        self.user_repository.get_current_user.assert_called_once_with(
            self.invalid_token
        )

    def test_get_current_user_v2_valid_token(self):
        self.user_repository.get_current_user.return_value = self.user
        self.use_case.get_current_user_v2(self.valid_token)
        # Verifica que el resultado sea None para que falle el test
        # self.assertIsNone(result)
        self.user_repository.get_current_user.assert_called_once_with(self.valid_token)

    def test_get_current_user_v2_invalid_token(self):
        self.user_repository.get_current_user.side_effect = HTTPException(
            status_code=401, detail="Invalid token"
        )
        with self.assertRaises(HTTPException):
            self.use_case.get_current_user_v2(self.invalid_token)
        self.user_repository.get_current_user.assert_called_once_with(
            self.invalid_token
        )


if __name__ == "__main__":
    unittest.main()
