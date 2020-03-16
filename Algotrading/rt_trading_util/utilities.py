import time
import math
import ciso8601
import itertools

import talib as tb
from talib import abstract
from talib.abstract import *
import datetime as dt

import matplotlib as mpl
from matplotlib import pyplot as plt

CURRENT_DATE = time.strftime("%x")

def dateToUNIX(date):  #format: "YYYYMMDD hhmmss"

	ts = ciso8601.parse_datetime(date)
	return time.mktime(ts.timetuple())

def UNIXtoDate(timestamp): return dt.datetime.fromtimestamp(timestamp)

def date2numWrapper(data): return mpl.dates.date2num(data)

def num2dateWrapper(data): return mpl.dates.num2date(data)

"""
def extendList(lagSize, listToExtend): 

    listToZip = [listToExtend for i in range(1, lagSize)]
    return list(itertools.chain.from_iterable(zip(*listToZip)))
"""
def extendList(listToExtend): return list(itertools.chain.from_iterable(zip(listToExtend, listToExtend)))

def RSI_IND(timeperiod, init):

    inputs = init
    return RSI(inputs, timeperiod)


def MOV_A(ma_type, timeperiod, init):

    inputs = init
    return MA(inputs, timeperiod, ma_type)

def BOL_BANDS(ma_type, nbdevup, nbdevdn, timeperiod, init):

    inputs = init
    upper, middle, lower = BBANDS(inputs, timeperiod, nbdevup, nbdevdn, ma_type)
    return (upper, middle, lower)

def firstNotNAN(talibOutput):
    for i in range(len(talibOutput)):
        if (math.isnan(talibOutput[i]) == False): return talibOutput[i]

