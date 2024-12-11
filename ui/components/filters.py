from datetime import datetime

def get_oct_nov_dates(year=None):
    current_year = year if year else datetime.now().year
    oct_start = f"{current_year}-10-01"
    nov_end = f"{current_year}-11-30"
    return oct_start, nov_end
