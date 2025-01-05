import logging

from django.conf import settings
from django.db import connection
from django.db.models import Func, F, ExpressionWrapper, FloatField
from django.db.models.expressions import RawSQL

from expenses.models import Expense
from gastitis.exceptions import NoExpensesInChat, UserNotAuthorized, GoogleAPIConnectionError
from services.google_sheets import GoogleSheet

def only_beta_users(username):
    """
    Only allow beta users to perform this action.
    """
    if username not in settings.BETA_USERS:
        raise UserNotAuthorized()


class ExportExpenses:

    def __init__(self, user, group, **expense_filters):
        self.user = user
        self.group = group
        self.expense_filters = expense_filters

    async def get_expenses(self):
        """
        Export expenses to Google Sheet
        """
        group_expenses_qs = Expense.objects.filter(group=self.group, **self.expense_filters)
        group_expenses_qs = group_expenses_qs.select_related("user").prefetch_related("tags")
        group_expenses_qs = self._fix_qs_format_to_serialization(group_expenses_qs)

        if not await group_expenses_qs.aexists():
            raise NoExpensesInChat()

        return group_expenses_qs

    def _fix_qs_format_to_serialization(self, group_expenses_qs):
        db_backend = connection.vendor

        if db_backend == "postgresql":
            group_expenses_qs = group_expenses_qs.annotate(
                formatted_date=Func(
                    F("date"),
                    function="TO_CHAR",
                    template="TO_CHAR(%(expressions)s, 'YYYY/MM/DD')",

                )
            )
        else:
            # Assume SQLite db, TO_CHAR doesn't work
            group_expenses_qs = group_expenses_qs.annotate(
                formatted_date=RawSQL("'Error (not valid in sqlite)'", [])
            )

        group_expenses_qs = group_expenses_qs.annotate(
            amount_as_float=ExpressionWrapper(
                F("amount"),
                output_field=FloatField()
            )
        )

        group_expenses_qs = group_expenses_qs.values_list(
            "formatted_date",
            "user__username",
            "description",
            "amount_as_float",
        )

        return group_expenses_qs


    async def get_expenses_table(self):
        table = [["fecha", "usuario", "gasto", "monto"]]
        expenses = await self.get_expenses()

        async for expense in expenses:
            table.append(expense)

        return table

    async def export_to_google_sheet(self, table):
        url, name = self.get_sheet_url_and_name()

        sheet = GoogleSheet(url)
        worksheet_name = await sheet.save_data(name, table)

        return url, worksheet_name

    def get_sheet_url_and_name(self):
        # TODO: save urls in db by group
        url = "https://docs.google.com/spreadsheets/d/1YimK1TlwjzfbCPZIxrTVsNJAhbhe4RnFmvibdkJLvzg/edit?gid=1350094138#gid=1350094138"

        name = self.group.name

        return url, name

    async def run(self):
        """
        Get and export the expenses and return the message to send to the user
        """

        try:
            only_beta_users(self.user.username)
        except UserNotAuthorized:
            return "Este comando está en beta. Solo usuarios autorizados pueden ejecutarlo."

        expenses = await self.get_expenses_table()

        try:
            sheet_url, worksheet_name = await self.export_to_google_sheet(expenses)
        except GoogleAPIConnectionError:
            logging.exception("Google API error - Check your credentials")
            return "Hubo un problema al intentar exportar (Error de conexión con API Google)"
        except Exception:
            logging.exception("Unhandled error")
            return "Hubo un problema al intentar exportar."

        text = "Exportado con éxito!\n\n"
        text += f"- Link de la hoja de cálculo: {sheet_url} \n\n"
        text += f"- Nombre de la nueva pestaña: *\"{worksheet_name}\"*."

        return text

