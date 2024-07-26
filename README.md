# Hexagonal-API
API RESTful con FastAPI y SQLite, con autenticación y autorización (JWT), y pruebas unitarias (pytest). Implementada con Arquitectura Hexagonal, Vertical Slice y Screaming Architecture.

## Requisitos

- Python 3.9.6
- FastAPI
- SQLite
- Pydantic
- Pytest
- JWT
- Poetr

## Instalación y Ejecución

1. Clona el repositorio:
   ``` bash
   git clone git@github.com:lesmesl/hexagonal-api.git
   ```
2. Navega al directorio del proyecto:
   ``` bash
   cd hexagonal-api.git
   ```
3. Instala las dependencias:
   ``` bash
   poetry install
   ```
4. Crea el archivo de variables de entorno .env y agrega tus configuraciones:

   ``` bash
    DATABASE_URL=sqlite:///./test.db
    SECRET_KEY=tu_secreto
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
   ``
5. Realiza las migraciones:
   ``` bash
   alembic upgrade head
   ```
6. Iniciar el proyecto:
   ``` bash
   poetry run uvicorn app.main:app --reload --port 8000
   ```


## Pruebas
1. Ejecuta las pruebas unitarias:
   ``` bash
   pytest
   ```

## Estructura del Proyecto
``` bash
HEXAGONAL-API/
├── app/
│   ├── config/
│   │   ├── config.py                 # Configuración general de la aplicación y sus variables de entorno
│   │   ├── database.py               # Configuración de la base de datos y creación de sesiones
│   │   ├── security.py               # Configuración de seguridad (JWT, OAuth2, etc.)
│   │   ├── fastapi_config.py         # Configuración de FastAPI
│   │   ├── constants.py              # Constantes de la aplicación
│   │   ├── __init__.py               
│   ├── products/
│   │   ├── application/
│   │   │   ├── create_product.py     # Caso de uso para crear un nuevo producto
│   │   │   ├── update_product.py     # Caso de uso para actualizar un producto
│   │   │   ├── delete_product.py     # Caso de uso para eliminar un producto
│   │   │   ├── get_products.py       # Caso de uso para obtener productos
│   │   ├── domain/
│   │   │   ├── model_schemas.py             # Esquemas de Pydantic para productos
│   │   │   ├── repository_interface.py # Interfaces de repositorios para productos
│   │   ├── infrastructure/
│   │   │   ├── models.py             # Modelos de SQLAlchemy para productos
│   │   │   ├── repository.py         # Implementación del repositorio de productos
│   │   │   ├── router.py             
│   │   │   ├── __init__.py           
│   ├── users/
│   │   ├── application/
│   │   │   ├── register_user.py      # Caso de uso para registrar un nuevo usuario
│   │   │   ├── login_user.py         # Caso de uso para iniciar sesión de usuario
│   │   │   ├── get_user.py           # Caso de uso para obtener perfil de usuario
│   │   ├── domain/
│   │   │   ├── model_schemas.py            # Esquemas de Pydantic para usuarios
│   │   │   ├── repository_interface.py # Interfaces de repositorios para usuarios
│   │   ├── infrastructure/
│   │   │   ├── models.py             # Modelos de SQLAlchemy para usuarios
│   │   │   ├── repository.py         # Implementación del repositorio de usuarios
│   │   │   ├── router.py             
│   │   │   ├── __init__.py           # Archivo de inicialización del módulo infrastructure
│   ├── __init__.py                   
│   ├── main.py                       # Punto de entrada de la aplicación
├── tests/
│   ├── conftest.py                   # Configuraciones para las pruebas
│   ├── test_users.py                 # Pruebas para el módulo de usuarios
│   ├── test_products.py              # Pruebas para el módulo de productos
│   ├── test_routers_ping.py          # Pruebas para el router de ping
│   └── __init__.py                   # Archivo de inicialización para el módulo de pruebas
├── alembic/
│   ├── versions/                     # Carpeta donde se almacenan las migraciones
│   ├── env.py                        # Archivo de entorno para Alembic
│   └── script.py.mako                # Plantilla para scripts de migración
├── scripts/                          # Scripts de inicialización o mantenimiento
│   ├── init_db.py                    # Script para inicializar la base de datos
├── docs/                             # Documentación adicional
├── alembic.ini                       # Archivo de configuración de Alembic
├── pyproject.toml                    # Archivo de configuración de Poetry
├── README.md                         # Documentación del proyecto
├── .env                              # Archivo de variables de entorno
└── .env_example                      # Archivo de ejemplo de variables de entorno
``` 
