import scipy.io.wavfile as wav
import numpy
import sys


#arguments: 	filenames = a list of filenames
#returns: 	outputRate = sample rate
#		outputDataList = a list of numpy arrays
#		maxDataLength = longest length of numpy arrays in outputDataList
def readFiles (filenames):
		
	outputDataList = []
	
	for i in range(len(filenames)):
	   
		fileIn = filenames[i]
		rate, data = wav.read(fileIn)
		
		if i == 0:
			outputRate = rate
			maxDataLength = data.shape[0]
		else:
			if rate != outputRate:
				print "error: different sample rates"
				sys.exit
			if data.shape[0] > maxDataLength:
				maxDataLength = data.shape[0]
					
		outputDataList.append(data)
	
	return outputRate, outputDataList, maxDataLength


#arguments: 	inputDataList = a list of numpy arrays
#		maxDataLength = longest length of numpy arrays
#returns:	outputData = averaged data from numpy arrays in inputDataList
def mixInputs (inputDataList, maxDataLength):
  
	#randomise signal positions
  	for i in range(len(inputDataList)):
	  
		randPos = numpy.random.randint(0, maxDataLength - inputDataList[i].shape[0] + 1)
		
		inputDataList[i] = numpy.lib.pad(inputDataList[i], (randPos, maxDataLength - inputDataList[i].shape[0] - randPos), 'constant', constant_values=(0.0, 0.0))
		
	#mix signals
	averagingCoefficient = 1.0 / len(inputDataList)
	outputData = numpy.zeros(inputDataList[0].shape[0])
	
	for i in inputDataList:	
		outputData = numpy.add(outputData, i * averagingCoefficient)	#average the amplitudes
		
	print "mixing completed"
	return outputData


#arguments: 	inputData = numpy array 
#		delay = delay in samples 
#		decay = measure of how much energy is lost on reverberation (0.0 - 1.0)(0.0 = full reverb, 1.0 = no reverb)
#		reverberations = number of "bounces"
#returns:	outputData = data with added reverb
def addReverb (inputData, delay, decay, reverberations):
	
	outputData = numpy.zeros(inputData.shape[0])
	
	for i in range(inputData.shape[0]):
	  
		outputData[i] += inputData[i]
		
		for j in range(reverberations):
			
			if (i + delay * j) < inputData.shape[0]:
				outputData[i + delay * j] += inputData[i] * ((1.0 - decay) ** j) 
	
	print "adding reverb completed"
	return outputData
      
#arguments: 	data = numpy array 
#returns:	data = numpy array
def normalise (data):
  
	data /= numpy.max(numpy.abs(data), axis = 0)
	
	print "normalising completed"
	return data



















