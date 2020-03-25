from tinyUtils import listUtils, timeUtils

fooList = [2, 4, 506, 9, 11, None, 8.900]
booList = [[1, 2, 3, 4, 5], [6, 7, 8, 9]]

print(listUtils.filterListByType(fooList, int))
print(listUtils.flattenList(booList))
print(listUtils.extendList(fooList, 2))