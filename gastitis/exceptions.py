class NoExpensesInChat(Exception):
    """
    No expenses created yet in current chat.
    """


class UserNotAuthorized(Exception):
    """
    The user is not authorized to perform this action.

    Commonly used for beta commands.
    """


class GoogleAPIConnectionError(Exception):
    """
    Credentials are not defined or there is another error with Google API
    """
