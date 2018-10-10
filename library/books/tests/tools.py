from datetime import datetime

def make_random_number():
    today = datetime.today()
    return str(today.hour) + str(today.min) + str(today.second) +str(today.microsecond)