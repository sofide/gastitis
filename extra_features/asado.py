import math


# map asado items to the calc of how much to buy for each of them
ITEMS_TO_BUY = {
    "choris": lambda people: math.ceil(0.5 * people),
    "morcillas": lambda people: math.ceil(0.5 * people),
    "churrasquitos de cerdo": lambda people: math.ceil(0.33 * people),
    "kg de costilla": lambda people: round(0.2 * people, 1),
    "kg de vacío": lambda people: round(0.2 * people, 1),
}

def how_much_asado_message(people: int):
    """
    Calculate how much asado to buy for the given number of people and create
    a friendly message.

    args:
        people (int): quantity of people that will eat the asado

    returns:
        str: message indicating how much asado to buy
    """
    if people <= 2:
        return "Este bot sabe calcular asado para 3 o más personas"

    message = f"Lista de compra para {people} personas:\n"

    for what_to_buy, how_much in ITEMS_TO_BUY.items():
        message += f"- {how_much(people)} {what_to_buy}\n"

    return message
