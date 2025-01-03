from django.db.models import Func, F, ExpressionWrapper, FloatField

from expenses.models import Expense
from gastitis.exceptions import NoExpensesInChat
from services.google_sheets import GoogleSheet


class ExportExpenses:

    def __init__(self, group, **expense_filters):
        self.group = group
        self.expense_filters = expense_filters

    async def get_expenses(self):
        """
        Export expenses to Google Sheet
        """
        group_expenses_qs = Expense.objects.filter(group=self.group, **self.expense_filters)
        group_expenses_qs = group_expenses_qs.select_related("user").prefetch_related("tags")

        group_expenses_qs = group_expenses_qs.annotate(
            formatted_date=Func(
                F("date"),
                function="TO_CHAR",
                template="TO_CHAR(%(expressions)s, 'YYYY-MM-DD')",

            )
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

        if not await group_expenses_qs.aexists():
            raise NoExpensesInChat()

        return group_expenses_qs

    async def get_expenses_table(self):
        table = [["fecha", "usuario", "gasto", "monto"]]
        expenses = await self.get_expenses()

        async for expense in expenses:
            table.append(expense)

        return table

    async def export_to_google_sheet(self, table):
        url = "https://docs.google.com/spreadsheets/d/1YimK1TlwjzfbCPZIxrTVsNJAhbhe4RnFmvibdkJLvzg/edit?gid=1350094138#gid=1350094138"
        sheet = GoogleSheet(url)
        await sheet.save_data("name", table)

    async def run(self):
        """
        Get and export the expenses and return the message to send to the user
        """
        expenses = await self.get_expenses_table()


        for e in expenses:
            print(e)
            print("--")

        await self.export_to_google_sheet(expenses)

        return "done"
