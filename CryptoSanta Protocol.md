# CryptoSanta Protocol

En este documento se describe el protocolo utilizado en la aplicación web «Secret Santa».

## ¿Qué datos se protegen? ¿Cuándo, dónde y cómo?

Antes de implementar un protocolo de seguridad, es necesario saber cuál es la información que se quiere mantener secreta, y determinar dónde y en qué momentos se debe resguardar. Sólo entonces puede comenzar a diseñarse el sistema.

En el caso de esta aplicación, la información confidencial del juego es quién es el amigx secretx de cada participante. Es decir, para cualquier adversario (con tiempo y recursos razonables) que intercepte mensajes entre los clientes y el servidor, o que obtenga acceso no autorizado a la base de datos, debe ser difícil recuperar dicha información.


## Protocolo/Operación del Sistema

### Creación de Usuario

1. El usuario llena un formulario de registro entregando su **username**, **email** y **password**.
2. En el lado del cliente (usando la WebCrypto API) se genera un par de claves pública y privada, y se produce un archivo que contiene cada una.
3. El usuario descarga dichos archivos y los guarda en un lugar seguro. *(Q: ¿Sería buena idea encriptar la clave privada con la misma contraseña del usuario?)*
4. Una vez que descarga los archivos se habilita el botón de registro.
5. El usuario presiona el botón de registro y se envía los datos del formulario, junto con su clave **pública**. (El backend de seguridad de Django se encarga de guardar la **password** de forma segura en la base de datos. La clave pública se almacena en texto plano).

### Creación de Evento

1. El usuario organizador del evento inicia sesión en el sistema con su **username** y su **password**.
2. En su dashboard, presiona el botón «Crear Evento».
3. En la vista de creación, indica un **título** para el evento.
4. El organizador invita a usuarios al evento, buscándolos por su **username**.

### Aceptar Invitación

1. Un usuario inicia sesión en el sistema con su **username** y su **password**.
2. En su dashboard puede ver una lista con todos los eventos en los que participa o a los que está invitado.
3. El usuario hace click en un evento al que está invitado, y en la vista que se abre puede aceptar la invitación, agregando así su clave pública.
4. El sistema marca su invitación como aceptada/confirmada, y pasa a ser un miembro del evento. En caso de rechazar, simplemente se elimina el participante creado al invitar.

### Iniciar Sorteo

1. El organizador de un evento se autentifica en el sitio.
2. En su dashboard, hace click en el evento para ir a la vista de detalles.
3. En la vista de detalles presiona un botón para iniciar el sorteo.
4. El servidor verifica que al menos 3 participantes del evento hayan aceptado su invitación; de lo contrario indica al organizador que no se puede iniciar el sorteo.
5. Si hay suficientes participantes, el servidor elimina a aquellos que no aceptaron su invitación.
6. Se revuelve una lista con los $n$ participantes que sí aceptaron la invitación.
7. Por cada participante $p_i$ de la lista revuelta, el servidor realiza lo siguiente:
    1. Genera una clave simétrica $k$ para el algoritmo AES-CTR.
    2. Obtiene la clave pública $pk_i$ de $p_i$.
    3. Calcula $event \textunderscore key=RSA-OAEP_{pk_i}(k)$ y la guarda en el campo `event_key` del participante $p_i$.
    4. El amigo secreto (gifter) de $p_i$ es $p_{(i-1) mod n}$ (donde el módulo cubre el caso de ser el primero en la lista y tratar de buscar el elemento anterior), y su clave pública es $gifter \textunderscore pk$.
    5. El participante que debe recibir un regalo (giftee) de $p_i$ es $p_{(i+1) mod n}$. Su nombre de usuario es $giftee \textunderscore id$ y su clave pública es $giftee \textunderscore pk$.
    6. Calcula $AES-CTR_{k}(giftee \textunderscore id)$ y guarda el resultado en el campo `giftee_id` de $p_i$.
    7. Calcula $AES-CTR_{k}(giftee \textunderscore pk)$ y guarda el resultado en el campo `giftee_pk` de $p_i$.
    8. Calcula $AES-CTR_{k}(gifter \textunderscore pk)$ y guarda el resultado en el campo `gifter_pk` de $p_i$.
8. El servidor descarta $k$.

