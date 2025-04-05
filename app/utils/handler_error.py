import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status
from functools import wraps

# Configure root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def handle_db_exceptions(rollback_on_fail: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)

            except HTTPException as http_exc:
                logger.warning(f"[{func.__name__}] HTTPException: {http_exc.detail}")
                raise http_exc

            except IntegrityError as integrity_err:
                if rollback_on_fail:
                    await self.db.rollback()

                error_message = str(integrity_err.orig).lower()

                # Determine user-friendly error
                if "duplicate key value violates unique constraint" in error_message:
                    if "label_id" in error_message:
                        detail = "A label with this ID already exists."
                    elif "box_id" in error_message:
                        detail = "This box already has a label assigned."
                    else:
                        detail = "Duplicate value violates a unique constraint."
                elif "foreign key constraint" in error_message or "violates foreign key constraint" in error_message:
                    detail = "foreign key reference"

                else:
                    detail = "Database integrity constraint violated."

                logger.error(f"[{func.__name__}] IntegrityError: {detail}", exc_info=True)

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=detail,
                )

            except SQLAlchemyError as db_exc:
                if rollback_on_fail:
                    await self.db.rollback()
                logger.error(f"[{func.__name__}] SQLAlchemyError: {str(db_exc)}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="A database error occurred.",
                )

            except Exception as exc:
                logger.exception(f"[{func.__name__}] Unexpected error: {str(exc)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Unexpected error: {str(exc)}",
                )
        return wrapper
    return decorator
