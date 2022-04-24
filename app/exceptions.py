from pydantic import BaseModel


class UserError(BaseModel):
    status_code: int = 500
    error_code: str
    error_msg: str


def unexpected_err(e: Exception):
    """
    Handles errors from external services
    """
    return UserError(error_code="0001", error_msg=str(e))


FileNotFoundErr = UserError(status_code=404, error_code="0002", error_msg="File not found")

ImageNotFoundErr = UserError(status_code=404, error_code="0003", error_msg="Image not found")