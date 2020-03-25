
import sys
import datetime

input = open(sys.argv[1], "r")
input = input.read().split('\n') #break up by newline
toTimestamp = lambda ts: datetime.datetime.strptime(ts,"%Y-%m-%dT%H:%M:%SZ").timestamp()

spaceSplitInputs = [i.split(" ") for i in input][::-1] #reversed
startTime = toTimestamp(spaceSplitInputs.pop()[0])
endTime = toTimestamp(spaceSplitInputs.pop()[0])

validMessages = []
for value in spaceSplitInputs:
	for word in value:
		tabSplit = word.split('\t')
		for t in tabSplit:
			try:
				validTimestamp = toTimestamp(t)
				if (validTimestamp >= startTime and validTimestamp <= endTime):
					valueToString = " ".join(value)
					validMessages.append(valueToString)
			except ValueError:
				continue

print(validMessages)



