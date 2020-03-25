from dateutil import relativedelta
from datetime import datetime
import itertools as itert
import matplotlib as mpls
import datetime as dt
import ciso8601
import time

class listUtils(object):

	def __init__(self, arg): pass

	@staticmethod
	def filterListByType(data, dataType):
		return list(filter(lambda x: isinstance(x, dataType), data))

	@staticmethod
	def flattenList(listToFlatten):

		if (len(listToFlatten) == 0): return listToFlatten
		return [item for sublist in list(listToFlatten) for item in sublist]

	@staticmethod
	def extendList(listToExtend, extenMultiplier): 

		extendedListTuple = tuple(itert.repeat(listToExtend, extenMultiplier))
		return list(itert.chain.from_iterable(zip(*extendedListTuple)))

class timeUtils(object):

	def __init__(self): pass

	@staticmethod
	def getCurrentTime():
		return str(datetime.now())

	@staticmethod
	def getCurrentDateStr():
		return time.strftime("%Y%m%d")

	@staticmethod
	def getCurrentTimeUNIX():
		return time.time()

	@staticmethod
	def dateToUNIX(date): #format: "YYYYMMDD hhmmss"
		ts = ciso8601.parse_datetime(date)
		return time.mktime(ts.timetuple())

	@staticmethod
	def UNIXtoDate(timestamp): 
		return dt.datetime.fromtimestamp(int(timestamp))

	@staticmethod
	def stringToDatetime(string): #format: "YYYYMMDD", ex: "20170519"
		return UNIXtoDate((dateToUNIX(string)))

	@staticmethod
	def date2numWrapper(data): 
		return mpl.dates.date2num(data)

	@staticmethod
	def num2dateWrapper(data): 
		return mpl.dates.num2date(data)

	@staticmethod
	def datetimeDiff(datetime1, datetime2):
		return relativedelta.relativedelta(datetime2, datetime1).days