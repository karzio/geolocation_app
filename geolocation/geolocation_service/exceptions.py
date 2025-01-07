class ExternalAPIError(Exception):
    """
    Raised when the API does not return success status code.
    """

    pass


class ResourceNotFoundError(Exception):
    """
    Raised when the requested web address is not found.
    """

    pass
