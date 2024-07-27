# Hexagonal-API
API RESTful con FastAPI y SQLite, con autenticación y autorización (JWT), y pruebas unitarias (pytest). Implementada con Arquitectura Hexagonal, Vertical Slice y Screaming Architecture.

## Requisitos

- Python 3.9.6
- FastAPI
- SQLite
- Pydantic
- Pytest
- JWT
- Poetry

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
2. Ejecuta el linter y formateador de código:
   ``` bash
   poetry run lint_and_format
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
│   │   │   ├── use_cases.py          # Contiene los diferentes casos de uso de productos
│   │   ├── domain/
│   │   │   ├── model.py                  # Contiene la entidad que define el producto
│   │   │   ├── repository_interface.py   # Interfaces de repositorios para productos
│   │   ├── infrastructure/
│   │   │   ├── models.py             # Modelos de SQLAlchemy para productos
│   │   │   ├── repository.py         # Implementación del repositorio de productos
│   │   │   ├── dtos.py               # schemas de Pydantic para base de datos de productos
│   │   │   ├── router.py             # Rutas del API para productos
│   │   │   ├── __init__.py           
│   ├── users/
│   │   ├── application/
│   │   │   ├── use_cases.py          # Contiene los diferentes casos de uso de usario
│   │   ├── domain/
│   │   │   ├── model.py                  # Contiene la entidad que define el usuario
│   │   │   ├── repository_interface.py   # Interfaces de repositorios para usuarios
│   │   ├── infrastructure/
│   │   │   ├── models.py             # Modelos de SQLAlchemy para usuarios
│   │   │   ├── repository.py         # Implementación del repositorio de usuarios
│   │   │   ├── dtos.py               # schemas de Pydantic para base de datos de usuarios
│   │   │   ├── router.py             # Rutas del API para usuarios
│   │   │   ├── __init__.py           
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
│   ├── lint_and_format.py.py         # Script de desarrollo para aplicar linter y formateer
├── docs/                             # Documentación adicional
├── alembic.ini                       # Archivo de configuración de Alembic
├── pyproject.toml                    # Archivo de configuración de Poetry
├── README.md                         # Documentación del proyecto
├── .env                              # Archivo de variables de entorno
└── .env_example                      # Archivo de ejemplo de variables de entorno
``` 
