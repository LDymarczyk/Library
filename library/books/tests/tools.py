from datetime import datetime

def make_random_number():
    today = datetime.today()
    #import pdb; pdb.set_trace()
    return str(today.hour) + str(today.minute) + str(today.second) +str(today.microsecond)