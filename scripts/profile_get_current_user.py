import cProfile
import io
import os
import pstats
import sys
import time

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session

from app.config.database import get_db
from app.users.application.use_cases import UserUseCase
from app.users.infrastructure.repository import UserRepository

# Inicializa la sesión de la base de datos
db: Session = next(get_db())

# Inicializa user_repository con la implementación concreta
user_repository = UserRepository(db)

# Reemplaza "your_valid_jwt_token" con un token JWT válido para pruebas
valid_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzIyMTQ4NTY4fQ.EiSljoQW60Y-C8YosKnzxwUGn30tBGKWqj-jgjN9Oh0"


def profile_get_current_user_v1():
    use_case = UserUseCase(user_repository)
    use_case.get_current_user_v1(valid_jwt_token)


def profile_get_current_user_v2():
    use_case = UserUseCase(user_repository)
    use_case.get_current_user_v2(valid_jwt_token)


def run_profile(func, func_name):
    pr = cProfile.Profile()
    pr.enable()
    start_time = time.time()
    func()
    end_time = time.time()
    pr.disable()

    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()

    with open(f"profile_{func_name}.txt", "w") as f:
        f.write(s.getvalue())

    # print(f"Profile for {func_name}:")
    # print(s.getvalue())
    print(f"{func_name} took {end_time - start_time} seconds")


# Ejecutar el perfilado para get_current_user_v1
run_profile(profile_get_current_user_v1, "get_current_user_v1")

# Ejecutar el perfilado para get_current_user_v2
run_profile(profile_get_current_user_v2, "get_current_user_v2")
