# Pasos seguidos

Solo estoy anotando los comandos que usé en la consola en caso de que se necesite rehacer algún paso. Después se puede reusar para hacer el README.

En Visual Studio Code (Windows), siguiendo las instrucciones de [aquí](https://tutorial.djangogirls.org/es/django_installation/).


## Instalación

1. Crear virtualenv:
```bash
python -m venv myvenv
```

2. Iniciar entorno:
    ```bash
    . myvenv\Scripts\activate.ps1
    ```
    (Usar `deactivate` para salir).

3. Actualizar pip:
```bash
python -m pip install --upgrade pip
```

4. Instalar Django:
```bash
pip install -r requirements.txt
```


## Iniciar proyecto

(Recordar tener el entorno iniciado).

1. Crear archivos del proyecto:
```bash
django-admin.exe startproject criptosanta_app .
```

2. Configurar base de datos:
```bash
python manage.py migrate
```

3. Iniciar el servidor:
```bash
python manage.py runserver
```


## Crear modelos

La idea sería tener instancias de amigo secreto (¿party, group, event?), los que debieran incluir:

| Propiedades Event | Nombre clase/variable | Notación en enunciado | Descripción |
|:-----------------:|:---------------------:|:---------------------:|-------------|
| Título | `title` | - | El nombre que le pondrán I guess |
| Fecha del evento | `event_date` | - | Cuándo se llevará a cabo |
| Grupo | `members` | "cada participante" | El conjunto de usuarios que participará |
| Claves | `pkey_list` | "bolsita" | La lista anónima de claves públicas de todos los participantes |

Y los usuarios (posiblemente ya está implementado en el framework) a su vez tendrán:

| Propiedades User | Nombre clase/variable | Notación en enunciado | Descripción |
|:----------------:|:---------------------:|:---------------------:|-------------|
| Nombre de usuario | `username` | - | Nombre dentro de la app |
| Contraseña | `password` | - | Para iniciar sesión |
| Preferencias | `likes` | - | Una lista que puede usarse de ideas de regalo o algo similar |
| Clave pública anónima | `pka` | "$`pk_a`$ propio" | Para que otros se puedan poner en contacto con éste |
| Clave privada anónima | `ska` | "$`sk_a`$ propio" | Para desencriptar los mensajes anónimos que recibe |

Para diferenciar un usuario de la app de un usuario en un evento (pues cada instancia de un amigo secreto involucraría un sorteo nuevo, y un mismo usuario puede estar en todos los eventos navideños que quiera), también debiera haber una clase para "usuarios participantes".

| Propiedades Participant | Nombre clase/variable | Notación en enunciado | Descripción |
|:-----------------------:|:---------------------:|:---------------------:|-------------|
| Usuario | `User` | "participante $`A_i`$" | El objeto `User` asociado, para tener acceso a su par de claves dentro de un evento |
| Clave amigo anónimo | `gifter_pka` | "$`pk_a`$ de su amigo secreto" | La clave pública del amigo secreto que le hará regalo (gifter) una vez que inicia un evento |
| Clave pública sorteo | `gifter_prk` | "$`pk^i`$ generado" | La clave pública para establecer contacto con su amigo secreto (gifter) computando su propio $`c_i`$ *(gifter public raffle key)* |
| Clave privada sorteo | `gifter_srk` | "$`sk^i`$ generado" | La clave privada para desencriptar al comunicarse con su amigo secreto (gifter) de forma directa *(gifter secret raffle key)* |
| Clave amigo conocido | `giftee_pka` | "$`pk^i`$ encontrado" | La clave pública del amigo secreto al que le tocó regalar (giftee), obtenida a partir del mensaje encriptado $`c_i`$ que solo éste sabe desencriptar con su $`sk_a`$ propio |
| ID amigo conocido | `giftee_id` | "amigo secreto $`A_i`$" | Identidad del amigo secreto (giftee), obtenida a partir del mensaje encriptado $`c_i`$. Sería básicamente todo lo que esté en su User que no sean claves/contraseñas XD (en caso de que hayan perfiles, PFP, etc.) |

1. Crear una aplicación para el juego:
```bash
python manage.py startapp santa_raffle
```

2. Generar tablas de los modelos:
```bash
python manage.py makemigrations santa_raffle
```

3. Definir otra app para crear un usuario custom:
```bash
python manage.py startapp accounts
python manage.py makemigrations accounts
python manage.py migrate accounts
```

4. Aplicar los cambios del modelo a la base de datos del proyecto entero:
```bash
python manage.py migrate
```

5. Crear superusuario: (para acceder a admin y ver los modelos)
    ```bash
    python manage.py createsuperuser
    ```
    (Hice uno para mí no más. Al ejecutar pide username, mail y pass).
    Con `python manage.py runserver`, y accediendo a http://127.0.0.1:8000/admin se llega a la pantalla de inicio de sesión.