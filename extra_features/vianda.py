"""
Utilities to calc the cost of viandas (usualy pay once a week)
"""

class MissingViandasOrDeliveries(Exception):
    """
    Param viandas or deliveries is missing.
    """


class InvalidViandasArguments(Exception):
    """
    User arguments are invalid.
    """


class ViandaCostCalculator:
    """
    Calc the vianda cost, considering by default a week of viandas (5 days) with
    2 viandas per day.
    """

    FOOD_COST = 5000
    DELIVERY_COST = 900
    COSTS_LAST_UPDATED = "2025/02/09"

    DEFAULT_DAYS = 5
    DEFAULT_VIANDAS_PER_DAY = 2


    def __init__(self, days=DEFAULT_DAYS, viandas=None, deliveries=None):
        if not viandas and not deliveries:
            viandas = self.DEFAULT_VIANDAS_PER_DAY * days
            deliveries = days
        elif (viandas and not deliveries) or (deliveries and not viandas):
            raise MissingViandasOrDeliveries(
                "viandas and deliveries should both have a value or neither"
            )

        self.viandas = viandas
        self.deliveries = deliveries

    def calc_cost(self):
        food_cost = self.viandas * self.FOOD_COST
        delivery_cost = self.deliveries * self.DELIVERY_COST

        cost = food_cost + delivery_cost

        return cost



class ViandaMessage:
    """
    Calc viandas cost and return a message for users.
    """

    def __init__(self, *args):
        self.args = args

    def get_viandas_calculator(self):
        """
        Based on user args, return the params needed to initialize ViandaCostCalculator.
        """
        match len(self.args):
            # case no arguments: use default values
            case 0:
                return ViandaCostCalculator()

            # case one argument: interpret as days
            case 1:
                try:
                    days = int(self.args[0])
                except ValueError as exc:
                    raise InvalidViandasArguments() from exc

                return ViandaCostCalculator(days=days)

            # case two arguments: interpret as viandas and deliveies
            case 2:
                viandas, deliveries = self.args
                try:
                    viandas = int(viandas)
                    deliveries = int(deliveries)

                except ValueError as exc:
                    raise InvalidViandasArguments() from exc

                return ViandaCostCalculator(viandas=viandas, deliveries=deliveries)

        # more than 2 args is an error
        raise InvalidViandasArguments()


    def message(self):
        try:
            calc = self.get_viandas_calculator()
        except InvalidViandasArguments:
            message = [
                f"Los parámetros {self.args} no son válidos.",
                "",
                "- Si no indicas parámetros se tomarán los valores por default.",
                "- Si indicas un parámetro se interpreta como cantidad de días",
                "- Si indicas dos parámetros se interpreta como cantidad de viandas y deliveries",
            ]

            return "\n".join(message)


        cost = calc.calc_cost()
        message = [
            f"TOTAL ${cost}",
            "",
            "Para el cálculo se consideró:",
            f"- {calc.viandas} viandas (${calc.FOOD_COST} c/u)",
            f"- {calc.deliveries} envíos (${calc.DELIVERY_COST} c/u)",
            "",
            f"Última actualización de costos: {calc.COSTS_LAST_UPDATED}",
        ]

        message = "\n".join(message)

        return message
