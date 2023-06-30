# Entrega Parcial

## Instalación
TODO (Link al otro `.md`?)

## Contexto
Explicar el secret santa y el esquema propuesto.

## Objetivos
1. Crear una aplicación web que implemente un juego de amigo secreto que otorgue las siguientes garantías:
    - Ningún participante A puede obtener el nombre de su amigo secreto B (donde B le regala a A).
    - Las conversaciones entre los participantes deben ser privadas.
2. Un usuario puede crear eventos e invitar a otros usuarios registrados.
3. El organizador de un evento debe poder hacer el sorteo una vez que todos los invitados hayan aceptado participar.
4. Cada usuario tiene un _dashboard_ donde puede ver todos los eventos en los que participa.

## Avances

**Disclaimer**: En este momento estamos preparando el backend y asegurándonos que funcione. Aún no hemos implementado nada relacionado a criptografía, sólo tenemos un «esqueleto» primordial del algoritmo propuesto.

Cuando una persona se registra en el sistema, se generan y se almacenan una clave pública y una privada. Estas serán usadas para todos los eventos en los que participe. En particular y, de acuerdo con el algoritmo propuesto, la clave pública servirá como el identificador anónimo que se utiliza en el sorteo, y la privada se utilizará para desencriptar el mensaje inicial en el que se identifica la pesona a la que el usuario debe hacerle un regalo.

## Preguntas/Problemas

1. ¿Qué limitaciones tenemos para el uso de librerías criptográficas? Por ejemplo, encontramos [esta](https://cryptography.io/en/latest/) que ofrece implementaciones de algunas de las primitivas que vimos en el curso, pero también tiene implementaciones de mecanismos completos (e.g acuerdo de claves DH). ¿Podríamos usarla?
2. El chat tiene un potencial problema de anonimato, pues en un grupo de amigos que se conocen desde hace mucho tiempo es posible identificar con quién uno habla a partir de la manera en que se expresa (uso de palabras particulares, emojis). Es más, si el chat es completamente libre, una persona puede decirle directamente quién es a su interlocutor. Una potencial solución es implementar un chat con mensajes, preguntas y respuestas predeterminadas, diseñadas exclusivamente para clarificar preferencias. ¿Qué nos recomiendan?
3. Las claves privadas utilizadas deben quedar almacenadas en la base de datos, pero guardarlas en texto plano daría mucho poder al administrador o a alguien que obtenga acceso no autorizado a la BD. Por otro lado, si se guarda encriptada, ¿cuál debería ser la clave? 
