from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    urole: str
    first_name: Optional[str]
    second_name: Optional[str]
    email: str
    password: str
