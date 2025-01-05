class NoExpensesInChat(Exception):
    """
    No expenses created yet in current chat.
    """

class UserNotAuthorized(Exception):
    """
    The user is not authorized to perform this action.

    Commonly used for beta commands.
    """
