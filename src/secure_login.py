"""Demostración de autenticación segura frente a SQL Injection."""

import pymssql

SERVER = "localhost"
PORT = 1433
USER = "sa"
PASSWORD = "YourStrong!Passw0rd"
DATABASE = "DemoInjection"


def secure_login(username: str, password: str) -> bool:
    """Realiza la consulta usando parámetros, evitando la inyección."""
    with pymssql.connect(server=SERVER, port=PORT, user=USER, password=PASSWORD, database=DATABASE) as connection:
        with connection.cursor(as_dict=True) as cursor:
            query = (
                "SELECT Id, Username, FullName "
                "FROM dbo.Users "
                "WHERE Username = %s AND Password = %s"
            )
            print("Consulta enviada al servidor (parametrizada):")
            print(query)
            cursor.execute(query, (username, password))
            result = cursor.fetchall()
            return bool(result)


def main() -> None:
    print("--- Demo de inicio de sesión seguro ---")
    user = input("Usuario: ")
    pwd = input("Contraseña: ")
    if secure_login(user, pwd):
        print("Autenticación exitosa.")
    else:
        print("Credenciales inválidas.")


if __name__ == "__main__":
    main()
