"""
Create a DTO class. It can encapsulate validation logic, ensuring
that data entering a particular layer or component meets certain
criteria before being processed.
"""
from pydantic import BaseModel, ConfigDict, Field


class UserDTO(BaseModel):

    pk: int | None = None
    name: str = Field(max_length=50, min_length=2)

    model_config: ConfigDict = ConfigDict(  # type: ignore
        from_attributes=True,
    )
