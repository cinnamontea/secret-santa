# Entrega Parcial

## Instalación

Para ejecutar el proyecto es necesario seguir los siguientes pasos:

1. Clonar este repositorio en un directorio de su elección con el comando:
    ```
    git clone https://github.com/cinnamontea/secret-santa.git
    ```
2. Dentro del repositorio, ejecutar el siguiente comando para crear un ambiente virtual de Python.
    ```
    python -m venv ./.venv
    ```
    Para activar el ambiente en Windows con Powershell, ejecutar:
    ```
    ./.venv/Scripts/Activate.ps1
    ```
    En Linux, ejecutar:
    ```
    $ source ./.venv/bin/activate
    ```
3. Actualizar `pip`.
    ```
    python -m pip install --upgrade pip
    ```
4. Instalar dependencias.
    ```
    python -m pip install -r requirements.txt
    ```
5. Correr las migraciones de la base de datos.
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Si se desea acceder al área admin del sistema se puede crear un super usuario, ejecutando el siguiente comando y siguiendo los pasos que éste indica.
    ```
    python manage.py createsuperuser
    ```
7. Lanzar el servidor, y acceder al sitio en la URL que indican los mensajes que muestra el comando (en general `http://127.0.0.1:8000/`; agregar `admin` al final para llegar a su pantalla de inicio de sesión).
    ```
    python manage.py runserver
    ```
   

## Contexto
El «amigo secreto» (o «secret santa» en inglés), es un juego muy habitual en época navideña, en la que cada persona de un grupo debe hacerle un regalo a otra sin que esta sepa de quién proviene el presente. Toda persona debe recibir un regalo, y no puede regalarse a sí misma. Usualmente, se escriben los nombres de cada participante en trozos de papel, se introducen en un contenedor (un sombrero de viejito pascuero, por ejemplo), se revuelven, y cada persona saca un papel para saber a quién debe hacerle el regalo (con repetición en caso de que obtenga su propio nombre). En algunas variaciones del juego, cada persona debe entregar el regalo de forma anónima, y se acuerda un día en el que se reúnen, y donde cada uno le cuenta al resto lo que ha recibido e intenta adivinar quién es su «secret santa».

En este contexto, se pretende implementar un sistema que permita gestionar este juego agregando algunas funcionalidades extra y utilizando criptografía para proteger los secretos involucrados en esta actividad. Para esto se propone el siguiente algoritmo:
1. Cada participante deberá contar con un par de claves (pk<sub>a</sub>, sk<sub>a</sub>) que deben ser anónimas.
2. El sistema recolecta las claves públicas pk<sub>a</sub> (de forma anónima) y las revuelve en una lista.
3. Dada la lista aleatorizada de claves públicas anónimas, cada participante es capaz de reconocer su propia clave pero no la del resto. Luego, cada participante selecciona la clave que se encuentra justo antes que la suya (esto evita que una persona sea su propio amigo secreto).
4. Una vez que cada participante A<sup>i</sup> tiene la clave pública anónima pk<sub>a</sub> de su amigo secreto, genera una nuevo par de claves pública y privada (pk<sup>i</sup>, sk<sup>i</sup>) y computa el valor:

    c<sub>i</sub> := <b>Enc</b><sub>pka</sub>(A<sub>i</sub> || pk<sup>i</sup>)
   
   Es decir, genera un texto cifrado que sólo podrá ser desencriptado por su amigo secreto, en el cual le indica su identidad y una clave pública para que le envíen mensajes en caso de cualquier duda.
6. Se publican todos los c<sub>i</sub>, y cada participante busca el texto cifrado que desencripte mediante su sk<sub>a</sub>. Con esto, podrá saber a quién debe hacerle un regalo.

## Objetivos
Se pueden separar los objetivos del proyecto en dos partes:

1. Crear una aplicación web que implemente un juego de amigo secreto. Algunas de las propiedades más importantes que debe incluir son que:
    - Cualquier usuario puede crear eventos e invitar a otros usuarios registrados a unirse.
    - Una vez que todos los invitados hayan aceptado participar, el organizador de un evento debe poder iniciar el sorteo (entendiéndose como el momento de la recolección de los $p_k$ en una lista).
    - Cada usuario tiene un _dashboard_ donde puede ver todos los eventos en los que participa y enterarse cuando su amigo secreto ha sido definido.

2. La aplicación anterior debería otorgar las siguientes garantías, mediante lo aprendido en el curso:
    - Ningún participante A puede obtener el nombre de su amigo secreto B (donde B le regala a A).
    - Las conversaciones entre los participantes deben ser privadas.

## Avances

El lenguaje de programación elegido para el proyecto es Python. La aplicación web se está realizando en Django.

**Disclaimer**: En este momento estamos preparando el backend y asegurándonos que funcione. Aún no hemos implementado nada relacionado a criptografía, sólo tenemos un «esqueleto» primordial del algoritmo propuesto.

Se han implementado [modelos](./accounts/models.py) que representan a los usuarios del sistema y las claves criptográficas que están asociadas a cada uno de ellos. El modelo de usuarios es una clase custom basada en el usuario abstracto que provee django. Esto permite reutilizar campos y funcionalidad implementada por el framework. Por otro lado, se implementaron [modelos](./santa_raffle/models.py) para representar un juego (o evento) y sus participantes. Puede ver más detalles de los campos de cada modelo en las tablas que se presentan [aquí](./Pasos%20seguidos.md#crear-modelos).

En términos de comportamiento implementado, cuando se crea un usuario en el sistema, se generan objetos que representan a las claves pública y privada del usuario y se asocian a éste. Por el momento, no se está usando nigún algoritmo de generación de claves. Lo implementado sólo tiene como propósito verificar que las piezas del backend están funcionando como se espera.

Finalmente, se registraron los modelos que se deben mostrar en la página de administración, ocultando los campos a los que los administradores no deberían tener acceso (por ejemplo, los valores de las claves privadas asociadas a los usuarios).

## Preguntas/Problemas

Creamos una sección aparte con observaciones notadas al analizar el proyecto, para los que agradeceríamos feedback.

1. ¿Qué limitaciones tenemos para el uso de librerías criptográficas? Por ejemplo, encontramos [esta](https://cryptography.io/en/latest/) que ofrece implementaciones de algunas de las primitivas que vimos en el curso, pero también tiene implementaciones de mecanismos completos (e.g acuerdo de claves DH). ¿Podríamos usarla?
2. El chat tiene un potencial problema de anonimato, pues en un grupo de amigos que se conocen desde hace mucho tiempo es posible identificar con quién uno habla a partir de la manera en que se expresa (uso de palabras particulares, emojis). Es más, si el chat es completamente libre, una persona puede decirle directamente quién es a su interlocutor. Una potencial solución es implementar un chat con mensajes, preguntas y respuestas predeterminadas, diseñadas exclusivamente para clarificar preferencias. ¿Qué nos recomiendan?
3. Las claves privadas utilizadas deben quedar almacenadas en la base de datos, pero guardarlas en texto plano daría mucho poder al administrador o a alguien que obtenga acceso no autorizado a la BD. Por otro lado, si se guarda encriptada, ¿cuál debería ser la clave? 
