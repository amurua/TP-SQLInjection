"""Configuración compartida de conexión a la base de datos."""

from typing import Final

DB_CONFIG: Final[dict[str, object]] = {
    "server": "localhost",
    "port": 1433,
    "user": "sa",
    "password": "YourStrong!Passw0rd",
    "database": "DemoInjection",
}
