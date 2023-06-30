# Entrega Parcial

## Instalación
TODO (Recoger los pasos importantes para ejecutar del otro `.md`)

## Contexto
Explicar el secret santa y el esquema propuesto.

## Objetivos
Se pueden separar los objetivos en dos partes:

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

Cuando una persona se registra en el sistema, se generan y se almacenan una clave pública y una privada. Estas serán usadas para todos los eventos en los que participe. En particular y, de acuerdo con el algoritmo propuesto, la clave pública servirá como el identificador anónimo que se utiliza en el sorteo, y la privada se utilizará para desencriptar el mensaje inicial en el que se identifica la pesona a la que el usuario debe hacerle un regalo.

## Preguntas/Problemas

Creamos una sección aparte con observaciones notadas al analizar el proyecto, para los que agradeceríamos feedback.

1. ¿Qué limitaciones tenemos para el uso de librerías criptográficas? Por ejemplo, encontramos [esta](https://cryptography.io/en/latest/) que ofrece implementaciones de algunas de las primitivas que vimos en el curso, pero también tiene implementaciones de mecanismos completos (e.g acuerdo de claves DH). ¿Podríamos usarla?
2. El chat tiene un potencial problema de anonimato, pues en un grupo de amigos que se conocen desde hace mucho tiempo es posible identificar con quién uno habla a partir de la manera en que se expresa (uso de palabras particulares, emojis). Es más, si el chat es completamente libre, una persona puede decirle directamente quién es a su interlocutor. Una potencial solución es implementar un chat con mensajes, preguntas y respuestas predeterminadas, diseñadas exclusivamente para clarificar preferencias. ¿Qué nos recomiendan?
3. Las claves privadas utilizadas deben quedar almacenadas en la base de datos, pero guardarlas en texto plano daría mucho poder al administrador o a alguien que obtenga acceso no autorizado a la BD. Por otro lado, si se guarda encriptada, ¿cuál debería ser la clave? 
