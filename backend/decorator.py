"""
Decorator for handling exceptions in FastAPI routes.
"""

from functools import wraps

from fastapi import HTTPException
from fastapi import status as s


def handle_exception(f):
    """
    Decorator to handle exceptions in FastAPI routes.

    Args:
        f (function): The FastAPI route function to decorate.

    Returns:
        function: The decorated function with exception handling.
    """

    @wraps(f)
    async def wrapper(*args, **kwargs):
        limit = kwargs.get("limit")
        sort_by = kwargs.get("sortBy")
        order_by = kwargs.get("orderBy")

        if limit and limit < 1:
            raise HTTPException(
                status_code=s.HTTP_400_BAD_REQUEST,
                detail="Limit must be a positive integer.",
            )

        # TODO : Check if value is available
        if sort_by and sort_by not in [
            "country_name",
            "population_density",
            "area",
            "population",
            "region",
        ]:
            raise HTTPException(
                status_code=s.HTTP_400_BAD_REQUEST, detail="Invalid sort field."
            )

        if order_by and order_by not in ["1", "-1"]:
            raise HTTPException(
                status_code=s.HTTP_400_BAD_REQUEST, detail="Invalid sort order."
            )

        try:
            return await f(*args, **kwargs)

        except ValueError as error:
            raise HTTPException(status_code=s.HTTP_400_BAD_REQUEST, detail=str(error))

        except Exception as error:
            raise HTTPException(
                status_code=s.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
            )

    return wrapper
