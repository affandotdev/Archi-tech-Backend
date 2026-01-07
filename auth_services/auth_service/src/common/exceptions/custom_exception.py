from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Global exception handler for DRF.
    Works for all API views automatically.
    """

    # First, let DRF generate its normal error response
    response = exception_handler(exc, context)

    # If DRF already handled it
    if response is not None:
        return Response(
            {"status": "error", "message": response.data, "details": None},
            status=response.status_code,
        )

    # If it's an unhandled exception
    return Response(
        {"status": "error", "message": "Internal server error", "details": str(exc)},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
