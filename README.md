# Práctica: SQL Injection con SQL Server en Docker

Este repositorio contiene un entorno mínimo para demostrar una consulta vulnerable a **SQL Injection** y su mitigación utilizando **consultas parametrizadas** sobre Microsoft SQL Server ejecutándose en Docker.

## Contenido del repositorio

| Archivo | Descripción |
|---------|-------------|
| [`docker-compose.yml`](docker-compose.yml) | Orquesta el contenedor de SQL Server y expone el puerto `1433`. |
| [`sql/init.sql`](sql/init.sql) | Script que crea la base de datos `DemoInjection`, su tabla `Users` y datos de prueba. |
| [`src/config.py`](src/config.py) | Configuración compartida para conectarse a la base de datos desde los ejemplos. |
| [`src/vulnerable_login.py`](src/vulnerable_login.py) | Script en Python que concatena la entrada del usuario y permite la inyección SQL. |
| [`src/secure_login.py`](src/secure_login.py) | Variante corregida que utiliza sentencias preparadas con parámetros. |
| [`requirements.txt`](requirements.txt) | Dependencias de Python necesarias para ejecutar los ejemplos. |

## Preparación del entorno

1. **Iniciar SQL Server en Docker**

   ```bash
   docker compose up -d
   ```

2. **Esperar a que el contenedor esté saludable** (unos segundos). Verificar con:

   ```bash
   docker compose ps
   ```

3. **Ejecutar el script SQL de inicialización** (solo la primera vez o cuando se quiera recrear la BD):

   ```bash
   MSYS_NO_PATHCONV=1 docker compose exec sqlserver sqlcmd -S localhost -U sa -P 'YourStrong!Passw0rd' -i /sql/init.sql
   ```

4. **Instalar dependencias de Python** (en tu máquina host o en un entorno virtual):

   ```bash
   pip install -r requirements.txt
   ```

## Demostración de la vulnerabilidad

1. Ejecuta el script vulnerable:

   ```bash
   python src/vulnerable_login.py
   ```

2. Autentícate con un usuario válido (ej. `alice` / `alice123`) para comprobar que funciona correctamente.
3. Ahora intenta un ataque con las credenciales:

   ```text
   Usuario: alice
   Contraseña: ' OR 1=1 --
   ```

   El script construye la consulta concatenando los valores introducidos. La contraseña inyectada hace que la condición `OR 1=1` siempre sea verdadera, por lo que el atacante inicia sesión sin conocer la contraseña real.

   Ejemplo de consulta que se envía al servidor:

   ```sql
   SELECT Id, Username, FullName FROM dbo.Users WHERE Username = 'alice' AND Password = '' OR 1=1 --'
   ```

## Mitigación con consultas parametrizadas

1. Ejecuta la versión corregida:

   ```bash
   python src/secure_login.py
   ```

2. Usa las mismas credenciales maliciosas (`alice` / `' OR 1=1 --`). El motor de base de datos recibe la estructura de la consulta separada de los valores, por lo que el payload se trata como texto literal y no altera la lógica SQL. El resultado será `Credenciales inválidas.`

## Informe breve

- **Entorno utilizado:** Docker con la imagen oficial `mcr.microsoft.com/mssql/server:2022-latest` y scripts de Python ejecutados desde la máquina host utilizando la librería `pymssql`.
- **Pasos de reproducción:** levantar el contenedor, ejecutar `sql/init.sql` para preparar la base de datos y lanzar los scripts `src/vulnerable_login.py` y `src/secure_login.py` siguiendo las instrucciones anteriores.
- **Cambio aplicado:** la versión vulnerable construía la consulta con f-strings concatenando directamente `username` y `password`. La versión segura reemplaza esa concatenación por una sentencia preparada (`WHERE Username = %s AND Password = %s`) y pasa los valores como parámetros.
- **Por qué la corrección evita la inyección:** al usar parámetros, el driver envía la consulta precompilada al servidor y los valores de entrada no se interpretan como parte del código SQL, sino como datos. Esto impide que un atacante modifique la lógica de la consulta, aun cuando incluya caracteres especiales como `'`, `--` o `OR` en sus entradas.

## Limpieza del entorno

Cuando termines, puedes apagar el contenedor con:

```bash
docker compose down
```
