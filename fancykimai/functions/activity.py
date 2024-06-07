from fancykimai.functions.kimai import kimai_request
from fancykimai.functions.config import get_config
from iterfzf import iterfzf

def select_activity(ctx, param, value: str) -> str:
    '''
    Select an activity from the list of activities in Kimai and return the id
    '''
    default = get_config('activity')
    activities = kimai_request('api/activities')
    if value:
        # Check if value is in the id or name of the activities
        for activity in activities:
            if value == activity['id']:
                return activity['id']
            if value == activity['name']:
                return activity['id']
        # If not found, return an error
        raise ValueError('Activity not found')
    else:
        # If no value is given, but there's a default activity, return the id
        if default:
            return default
        # If no value is given and there's no default activity, prompt the user
        activity_names = [f"{activity['id']} - {activity['name']}" for activity in activities]
        selected_activity = iterfzf(activity_names)
        if selected_activity:
            return selected_activity.split(' - ')[0]
        else:
            raise ValueError('Activity not found')

