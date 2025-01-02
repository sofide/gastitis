"""
Texts for /help command.
"""
OPTIONAL_PARAMETERS = "_Parámetros opcionales:_"
SHORTCUT = "_Atajo_:"
EXAMPLE = "_Ejemplo_:"

HELP_GASTO = f"""
*Registrar un gasto:* `/gasto <monto> <descripcion>`

{SHORTCUT} `/g`

{OPTIONAL_PARAMETERS}
    - dd <fecha> en formato año/mes/día. Ej: `dd 2024/10/01`.
    - tt tag1,tag2,tag3. Ej: `tt comida` o `tt comida,salida`.
    - uu <usuario> que realizó el gasto. Ej: `uu juan`. (por default se carga el gasto a nombre de quien envía el mensaje).

Ejemplo con todos los params opcionales:
    `/gasto 10 pan  dd 2024/01/30 tt comida uu juan`
"""

HELP_TOTAL = """
*Ver el total hasta el momento:* `/total`
"""

HELP_MES = f"""
*Ver el total del mes actual:* `/mes`

{SHORTCUT} `/m`

{OPTIONAL_PARAMETERS}
    - `/mes <mes>` Ej: `/mes 5` para ver los gastos de mayo del año actual.
    - `/mes <mes> <año>` para ver los gastos del mes/año especificado.
"""

HELP_PAGO = f"""
*Registrar un pago a un usuario del grupo:* `/pago <username>`

_Esta funcionalidad solo está disponible en grupos con más de un usuario._

{SHORTCUT} `/p`

{OPTIONAL_PARAMETERS}
    - <fecha> Ej: `/pago @juan 2020/12/1`
"""

HELP_ASADO = f"""
*Calcular asado a comprar según la cantidad de personas:* `/asado <cantidad de personas>`

{SHORTCUT} `/a`

{EXAMPLE} `/asado 12` Para calcular cuánto asado comprar para 12 personas.
"""

HELP_TEXT = f"""Cómo usar gastitis:

{HELP_GASTO}
--------------------
{HELP_TOTAL}
--------------------
{HELP_MES}
--------------------
{HELP_PAGO}
--------------------
{HELP_ASADO}
"""
