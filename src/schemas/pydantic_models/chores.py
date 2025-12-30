from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field

class NewChoreModel(BaseModel):
    """
    name: str, description: str, point: int, group_id: int
    """
    name: str = Field(..., description="Name of the chore")
    description: Optional[str] = Field(default=None, description="Description of the chore")
    point: int = Field(..., description="Points awarded for completing the chore")
    group_id: int = Field(..., alias="groupId", description="ID of the group (family) the chore belongs to")
