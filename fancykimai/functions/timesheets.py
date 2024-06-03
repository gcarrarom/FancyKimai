from fancykimai.functions.kimai import kimai_request
from fancykimai.classes.kimai_types import TimesheetCollection
from pydantic import parse_obj_as
from typing import List

def get_timesheets(data=None) -> List[TimesheetCollection]:
    timesheets = kimai_request("api/timesheets", data=data)
    return [parse_obj_as(TimesheetCollection, timesheet) for timesheet in timesheets]

