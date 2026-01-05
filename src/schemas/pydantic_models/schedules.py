from datetime import datetime
from email.policy import default
from typing import Optional, Literal

from pydantic import BaseModel, Field

class NewScheduleModel(BaseModel):
    """
    """
    schedule_date: Optional[datetime] = Field(default=None, alias="scheduleDate", description="Date of the scheduled chore")
    chore_id: Optional[int] = Field(default=None, alias="choreId", description="ID of the chore to be assigned")
    new_chore_name: Optional[str] = Field(default=None, alias="newChoreName", description="Name of the chore to be assigned")
    member_id: int = Field(alias="memberId", description="ID of the member assigned to the chore")
    point: Optional[int] = Field(default=None, description="Points awarded for completing the chore")
    # status: str = Field(default="Pending", description="Status of the chore assignment", regex="^(Pending|InProgress|Done|FullyReviewed)$")
    status: Literal["Pending", "InProgress", "Done", "FullyReviewed"] = Field(default="Pending", description="Status of the chore assignment")
    comment: str | None = Field(None, description="Optional comment about the chore assignment")

    # allow population by field name or alias
    class Config:
        validate_by_name = True