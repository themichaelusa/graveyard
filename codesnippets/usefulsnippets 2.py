import datetime as dt
import ciso8601
import time

def stringToDatetime(string): #format: "YYYYMMDD hhmmss", ex: "20170519"

	raw_ts = ciso8601.parse_datetime(string)
	timestamp = time.mktime(ts.timetuple())
	return dt.datetime.fromtimestamp(int(timestamp))

def stringToUNIX(string): #format: "YYYYMMDD", ex: "20170519"

	raw_ts = ciso8601.parse_datetime(string)
	return time.mktime(ts.timetuple())

