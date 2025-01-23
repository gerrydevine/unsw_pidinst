'''
A collection of utility functions
'''

import datetime

def validate_date(date_text):
    ''' Validate that date string is YYYY-MM-DD '''
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")