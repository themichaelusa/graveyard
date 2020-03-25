def flattenList(listToFlatten):

	nestedList = any(isinstance(sl, list) for sl in listToFlatten) 
	if(nestedList == False): return listToFlatten
	return [item for sublist in list(listToFlatten) for item in sublist]