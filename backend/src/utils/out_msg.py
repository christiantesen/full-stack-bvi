from . import BaseModelConfig

"""
200

DE ACUERDO

Indica que las llamadas que no crean un objeto nuevo se han realizado correctamente.

201

Creado

Se ha creado correctamente un objeto. El encabezado de ubicación de la respuesta incluye el identificador único del objeto.

202

Aceptado

Se ha iniciado un trabajo en segundo plano para realizar la solicitud, pero aún no se ha completado.

400

Solicitud incorrecta

La entrada de la solicitud no se reconoce o no es apropiada.

401

No autorizado

Error en la autenticación del usuario.

403

Prohibido

Se deniega el acceso debido a un error de autorización.

404

No encontrado

El recurso al que se hace referencia en la solicitud no existe.

405

Método no permitido

El método HTTP de la solicitud no es compatible con el recurso.

409

Conflicto

Se ha producido un error al intentar crear un objeto porque primero se debe crear otro objeto o ya existe el objeto solicitado.

422

Entidad no procesable

500

Error interno

Se ha producido un error interno general en el servidor.
"""


class MsgResponse(BaseModelConfig.BaseResponse):
    msg: str

    class Config:
        json_schema_extra = {
            "example": {
                "msg": "Mensaje"
            }
        }