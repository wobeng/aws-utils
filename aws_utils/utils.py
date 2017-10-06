import os
import re
import traceback
from datetime import datetime, timedelta


def process_exception(e):
    traceback.print_exc()


# loop through dates
def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


# convert datetime to unix_time
def datetime_to_unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    output = int((dt - epoch).total_seconds() * 1000.0)
    return output


# Replace multiple patterns in a single pass
# Credit: Xavier Defrang, Alex Martelli

def make_xlat(*args, **kwargs):
    find_replace = dict(*args, **kwargs)
    rx = re.compile('|'.join(map(re.escape, find_replace)))

    def one_xlat(match):
        return find_replace[match.group(0)]

    def xlat(text):
        return rx.sub(one_xlat, text)

    return xlat


def import_env_vars(config):
    for k in config:
        os.environ[str(k)] = str(config[k])
