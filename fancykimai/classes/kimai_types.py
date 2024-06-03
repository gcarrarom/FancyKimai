from pydantic import BaseModel
from typing import List, Optional
from pydantic import Field

class TimesheetMeta(BaseModel):
    name: str
    value: str

class TimesheetCollection(BaseModel):
    activity: Optional[int]
    project: Optional[int]
    user: Optional[int]
    tags: Optional[List[str]]
    timesheet_id: int = Field(alias="id")
    begin: Optional[str]
    end: Optional[str]
    duration: Optional[int]
    description: Optional[str]
    rate: Optional[float]
    internalRate: Optional[float]
    exported: Optional[bool]
    billable: Optional[bool]
    metaFields: Optional[List[TimesheetMeta]]