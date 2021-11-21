"""
Custom exceptions for bot managing.
"""

class ParameterError(Exception):
    """
    Error in parameters received in a command.
    """
    pass


class DateFormatterError(Exception):
    """
    Error in date format
    """
    pass
