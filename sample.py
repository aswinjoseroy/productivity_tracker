from datetime import datetime
import pytz

tz_NY = pytz.timezone('Asia/Kolkata')
datetime_NY = datetime.now(tz_NY)

print datetime.now().strftime("%m/%d/%y")
