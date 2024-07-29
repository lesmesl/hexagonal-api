# Hexagonal-API
API RESTful con FastAPI y SQLite, con autenticación y autorización (JWT), y pruebas unitarias (pytest). Implementada con Arquitectura Hexagonal, Vertical Slice y Screaming Architecture.

<img src="docs/diagram_infra.jpeg" alt="Diagrama de arquitectura" width="300"/>

## Requisitos previos

- Python 3.9.6
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
   poetry run uvicorn app.main:app --reload --port 8001
   ```
7. Documentación de la API:
   ``` bash
   http://localhost:8001/docs
   ```


## Pruebas unitarias
1. Ejecuta las pruebas unitarias:
   ``` bash
   pytest
   ```

## Utilidades
1. Ejecuta el linter y formateador de código:
   ``` bash
   poetry run lint_and_format
   ```
2. Ruta de colecciones de documentación API Postman:
   ``` bash
   docs/collections/
   ```

 
## Estructura del Proyecto
``` bash
HEXAGONAL-API/
├── app/
│   ├── config/
│   │   ├── config.py                 # Declaración de las constantes y variables necesarias
│   │   ├── constants.py              # Definición de constantes utilizadas en la aplicación
│   │   ├── database.py               # Configuración de la base de datos y creación de sesiones
│   │   ├── error_handlers.py         # Manejadores de errores personalizados
│   │   ├── exceptions.py             # Definición de excepciones personalizadas
│   │   ├── fastapi_config.py         # Configuración específica de FastAPI
│   │   ├── security.py               # Configuración de seguridad (JWT, OAuth2, etc.)
│   ├── products/
│   │   ├── application/
│   │   │   ├── use_cases.py          # Casos de uso relacionados con productos
│   │   ├── domain/
│   │   │   ├── model.py              # Entidad que define el producto
│   │   │   ├── repository_interface.py # Interfaces de repositorios para productos
│   │   ├── infrastructure/
│   │   │   ├── dtos.py               # Schemas de Pydantic para productos
│   │   │   ├── models.py             # Modelos de SQLAlchemy para productos
│   │   │   ├── repository.py         # Implementación del repositorio de productos
│   │   │   ├── router.py             # Rutas del API para productos
│   ├── users/
│   │   ├── application/
│   │   │   ├── use_cases.py          # Casos de uso relacionados con usuarios
│   │   ├── domain/
│   │   │   ├── model.py              # Entidad que define el usuario
│   │   │   ├── repository_interface.py # Interfaces de repositorios para usuarios
│   │   ├── infrastructure/
│   │   │   ├── dtos.py               # Schemas de Pydantic para usuarios
│   │   │   ├── models.py             # Modelos de SQLAlchemy para usuarios
│   │   │   ├── repository.py         # Implementación del repositorio de usuarios
│   │   │   ├── router.py             # Rutas del API para usuarios
│   ├── __init__.py                   # Inicialización del paquete
│   ├── main.py                       # Punto de entrada de la aplicación
├── tests/
│   ├── conftest.py                   # Configuraciones para las pruebas
│   ├── application/                  # Pruebas relacionadas con la capa de aplicación
│   ├── config/                       # Pruebas relacionadas con la configuración
│   ├── infrastructure/               # Pruebas relacionadas con la infraestructura
│   └── __init__.py                   # Inicialización del paquete de pruebas
├── alembic/
│   ├── versions/                     # Carpeta donde se almacenan las migraciones
│   ├── env.py                        # Archivo de entorno para Alembic donde se indican los modelos a crear
│   └── script.py.mako                # Plantilla para scripts de migración
├── scripts/                          # Scripts de inicialización o mantenimiento
│   ├── lint_and_format.py            # Script de desarrollo para aplicar linter y formatear código
├── docs/                             # Documentación adicional
│   ├── collections/                  # Colecciones de documentación
│   ├── diagram_infra.png             # Diagramas de infraestructura
├── alembic.ini                       # Archivo de configuración de Alembic
├── pyproject.toml                    # Archivo de configuración de Poetry
├── README.md                         # Documentación del proyecto
└── .env_example                      # Archivo de ejemplo de variables de entorno
``` 
