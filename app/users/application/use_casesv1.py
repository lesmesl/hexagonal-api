from fastapi.security import OAuth2PasswordBearer

from app.config.config import settings
from app.users.domain.repository_interface import UserRepositoryInterface

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


class UserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    # def get_current_user_v1(self, token: str) -> UserResponseSchema:
    #     start_time = time.time()
    #     user = self.user_repository.get_current_user(token)
    #     result = UserResponseSchema.model_validate(user)
    #     end_time = time.time()
    #     print(f"get_current_user_v1 took {end_time - start_time} seconds")
    #     return result

    # def get_current_user_v2(self, token: str):
    #     start_time = time.time()
    #     result = self.user_repository.get_current_user("asdasdasdas")
    #     end_time = time.time()
    #     print(f"get_current_user_v2 took {end_time - start_time} seconds")
    #     return result
