"""
Decorator for handling session in DB transactions
"""

from sqlalchemy.exc import IntegrityError


def handle_session(f):
    """
    Handle session for DB transactions

    Args:
        f: function to be decorated

    Returns:
        wrapper function

    Raises:
        Exception: if there is an error in the transaction
    """

    def wrapper(self, *args, **kwargs):
        session = self.Session()
        try:
            result = f(self, session, *args, **kwargs)
            return result
        except IntegrityError as error:
            session.rollback()
            raise Exception("Integrity Error: {}".format(error))
        except Exception as error:
            session.rollback()
            raise Exception("Error: {}".format(error))
        finally:
            session.expunge_all()
            session.close()

    return wrapper
