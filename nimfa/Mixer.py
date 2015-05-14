import scipy.io.wavfile as wav
import numpy
import sys
import math


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
'''
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
'''


#arguments: 	inputData_1, inputData_2 = input numpy arrays
#		maxDataLength = longest length of numpy arrays
#               decibelAmplification = amplification of the signal added to the other channel in decibels
#returns:	outputData = numpy array (stereo signal)
def mixInputs (inputData_1, inputData_2, maxDataLength, decibelAmplification):
    
        additionCoefficient = 10 ** (decibelAmplification / 20.0)
    
        randPos = numpy.random.randint(0, maxDataLength - inputData_1.shape[0] + 1)
        inputData_1 = numpy.lib.pad(inputData_1, (randPos, maxDataLength - inputData_1.shape[0] - randPos), 'constant', constant_values=(0.0, 0.0))

        randPos = numpy.random.randint(0, maxDataLength - inputData_2.shape[0] + 1)
        inputData_2 = numpy.lib.pad(inputData_2, (randPos, maxDataLength - inputData_2.shape[0] - randPos), 'constant', constant_values=(0.0, 0.0))

        outputData_1 = inputData_1
        outputData_1 = numpy.add(outputData_1, additionCoefficient * inputData_2)
        
        outputData_2 = inputData_2
        outputData_2 = numpy.add(outputData_2, additionCoefficient * inputData_1)
        
        outputData = numpy.vstack(([outputData_1, outputData_2]))
        
        print "signal mixing decibel amplification: " + str(decibelAmplification)
        print "signal mixing addition coefficient: " + str(additionCoefficient)
        
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
#               decibelAmplification = amplification in decibels
#returns:	data = numpy array
def addNormalNoise (data, decibelAmplification):
    
    standardDeviation = 10 ** (decibelAmplification / 20.0)
    
    data += numpy.random.normal(0, standardDeviation, data.shape)
    
    print "normal noise decibel amplification: " + str(decibelAmplification)
    print "normal noise standard deviation: " + str(standardDeviation)
    
    return data

      
#arguments: 	data = numpy array 
#returns:	data = numpy array
def normalise (data):
  
    if data.shape[0] == 2:
        for i in range(data.shape[0]):
            
            data[i] /= numpy.max(numpy.abs(data[i]), axis = 0)
            
    else:
        data /= numpy.max(numpy.abs(data), axis = 0)
	
    print "normalising completed"
    return data



















