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
| Título | title | - | El nombre que le pondrán I guess |
| Fecha del evento | eventDate | - | Cuándo se llevará a cabo |
| Grupo | members | "cada participante" | El conjunto de usuarios que participará |
| Claves | pkeyList | "bolsita" | La lista anónima de claves públicas de todos los participantes |

Y los usuarios (posiblemente ya está implementado en el framework) a su vez tendrán:

| Propiedades User | Nombre clase/variable | Notación en enunciado | Descripción |
|:----------------:|:---------------------:|:---------------------:|-------------|
| Nombre de usuario | username | - | Nombre dentro de la app |
| Contraseña | password | - | Para iniciar sesión |
| Preferencias | likes | - | Una lista que puede usarse de ideas de regalo o algo similar |
| Clave pública anónima | pka | "$`pk_a`$ propio" | Para que otros se puedan poner en contacto con éste |
| Clave privada anónima | ska | "$`sk_a`$ propio" | Para desencriptar los mensajes anónimos que recibe |

Para diferenciar un usuario de la app de un usuario en un evento (pues cada instancia de un amigo secreto involucraría un sorteo nuevo, y un mismo usuario puede estar en todos los eventos navideños que quiera), también debiera haber una clase para "usuarios participantes".

| Propiedades Participant | Nombre clase/variable | Notación en enunciado | Descripción |
|:-----------------------:|:---------------------:|:---------------------:|-------------|
| Usuario | User | "participante $`A_i`$" | El objeto User asociado, para tener acceso a su par de claves dentro de un evento |
| Clave amigo anónimo | gifterPKA | "$`pk_a`$ de su amigo secreto" | La clave pública del amigo secreto que le hará regalo (gifter) una vez que inicia un evento |
| Clave pública sorteo | gifterPRK | "$`pk^i`$ generado" | La clave pública para establecer contacto con su amigo secreto (gifter) computando su propio $`c_i`$ *(gifter public raffle key)* |
| Clave privada sorteo | gifterSRK | "$`sk^i`$ generado" | La clave privada para desencriptar al comunicarse con su amigo secreto (gifter) de forma directa *(gifter secret raffle key)* |
| Clave amigo conocido | gifteePKA | "$`pk^i`$ encontrado" | La clave pública del amigo secreto al que le tocó regalar (giftee), obtenida a partir del mensaje encriptado $`c_i`$ que solo éste sabe desencriptar con su $`sk_a`$ propio |
| ID amigo conocido | gifteeID | "amigo secreto $`A_i`$" | Identidad del amigo secreto (giftee), obtenida a partir del mensaje encriptado c_i. Sería básicamente todo lo que esté en su User que no sean claves/contraseñas XD (en caso de que hayan perfiles, PFP, etc.) |

1. Crear una aplicación:
```bash
python manage.py startapp santa_raffle
```

2. 