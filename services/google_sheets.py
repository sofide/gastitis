"""
Integration with Google Sheets
"""
import asyncio
from functools import wraps

import gspread

CREDENTIALS_FILE = "gastitis/google_credentials.json"


def asyncify(func):
    """
    Decorator to run blocking functions asynchronously.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)
    return wrapper


class GoogleClient:
    @asyncify
    def _get_service_account(self):
        if not hasattr(self, "_service_account"):
            self._service_account = gspread.service_account(filename=CREDENTIALS_FILE)
        return self._service_account

    @asyncify
    def _get_sheet_from_google(self, service_account, sheet_url):
        return service_account.open_by_url(sheet_url)

    async def get_sheet(self, sheet_url):
        service_account = await self._get_service_account()
        return await self._get_sheet_from_google(service_account, sheet_url)

    @asyncify
    def create_empty_worksheet(self, sheet, worksheet_name):
        return sheet.add_worksheet(worksheet_name, rows=1, cols=1)

    @asyncify
    def save_data_in_worksheet(self, worksheet, data):
        worksheet.update(data, "A1")

google_client = GoogleClient()

class GoogleSheet:
    def __init__(self, sheet_url):
        self.sheet_url = sheet_url

    async def get_sheet(self):
        if not hasattr(self, "_sheet"):
            try:
                self._sheet = await google_client.get_sheet(self.sheet_url)
            except gspread.exceptions.SpreadsheetNotFound as exc:
                raise Exception("remember to share the sheet") from exc  #TODO: improve this
        return self._sheet


    async def create_new_worksheet(self, worksheet_name):
        sheet = await self.get_sheet()
        existing_worksheets = [w.title for w in sheet.worksheets()]

        worksheet_final_name = worksheet_name
        name_suffix = 0

        while worksheet_final_name in existing_worksheets:
            name_suffix += 1
            worksheet_final_name = f"{worksheet_name}-{name_suffix}"

        worksheet = await google_client.create_empty_worksheet(sheet, worksheet_final_name)

        return worksheet, worksheet_final_name

    async def save_data(self, worksheet_name, data):
        worksheet, worksheet_name = await self.create_new_worksheet(worksheet_name)

        await google_client.save_data_in_worksheet(worksheet, data)
