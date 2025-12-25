from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")

class BaseResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    errors: Optional[dict] = None
