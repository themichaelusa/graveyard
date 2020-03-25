import math
import numpy as np
from PIL import Image 
from sys import getsizeof

np.set_printoptions(threshold=np.nan)
img = Image.open("test.png")
width, height = img.size
colorSpaces = img.split()

def createColorChannels(colorSpaces, height, width):

	redChannel, greenChannel, blueChannel, alphaChannel = [],[],[],[]
	redSpace, greenSpace, blueSpace, alphaSpace = colorSpaces[0], colorSpaces[1], colorSpaces[2], colorSpaces[3]

	for i in range(height): # O(n^2) Runtime
		for j in range(width):
			redChannel.append(redSpace.getpixel((j,i)))
			greenChannel.append(greenSpace.getpixel((j,i)))
			blueChannel.append(blueSpace.getpixel((j,i)))
			alphaChannel.append(alphaSpace.getpixel((j,i)))

	fRedChannel = np.array(redChannel).reshape(width,height)
	fGreenChannel = np.array(greenChannel).reshape(width,height)
	fBlueChannel = np.array(blueChannel).reshape(width,height)
	fAlphaChannel = np.array(alphaChannel).reshape(width,height)

	return (fRedChannel, fGreenChannel, fBlueChannel, fAlphaChannel)


def findMinMaxRangeChannel(colorChannel):
	minValue, maxValue = np.amin(colorChannel), np.amax(colorChannel)
	return (minValue, maxValue, (maxValue - minValue))

# def searchForColorGradient():

def searchChannelForColor(colorChannel, colorValue):

	colorCoords = []
	for i in range(len(colorChannel[1])): # height
		for j in range(len(colorChannel[i])): #width
			if (colorChannel[j][i] == colorValue):
				colorCoords.append((j,i))

	return colorCoords

				  
colorChannels = createColorChannels(colorSpaces, height, width)
neuList = colorChannels[0][0][:15]
condensedRow = combineSameColor(neuList)
print (condensedRow)
# for i in range(15):
	# print (colorChannels[0][i][:15])

# blueChannelMixMax = findMinMaxRangeChannel(colorChannels[2])
# bigVal = math.pow(260570010867270, 1/5)
# print (bigVal)
# print (math.pow(bigVal, 5))
# print (getsizeof(bigVal))
# print (searchChannelForColor(colorChannels[2], 221))
# print (getsizeof(searchChannelForColor(colorChannels[2], 221)))