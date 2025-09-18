"""Demostración de autenticación vulnerable a SQL Injection."""

import pymssql

from config import DB_CONFIG


def insecure_login(username: str, password: str) -> bool:
    """Realiza una consulta insegura concatenando la entrada del usuario."""
    with pymssql.connect(**DB_CONFIG) as connection:
        with connection.cursor(as_dict=True) as cursor:
            query = (
                "SELECT Id, Username, FullName "
                "FROM dbo.Users "
                f"WHERE Username = '{username}' AND Password = '{password}'"
            )
            print("Consulta enviada al servidor (insegura):")
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            return bool(result)


def main() -> None:
    print("--- Demo de inicio de sesión inseguro ---")
    user = input("Usuario: ")
    pwd = input("Contraseña: ")
    if insecure_login(user, pwd):
        print("Autenticación exitosa (o el atacante explotó la vulnerabilidad).")
    else:
        print("Credenciales inválidas.")


if __name__ == "__main__":
    main()
