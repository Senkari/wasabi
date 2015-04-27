
import numpy
import scipy.stats


def cluster (signals):
	
	outputSignals = []
	passedThreshold = True
	
	i = 0
	while len(signals) > 0:
	  
		outputSignals.append(signals.pop(0))  
		
		while len(signals) > 0 and passedThreshold == True:
		
			signalSum, signals, passedThreshold = maxXcorSum(outputSignals[i], signals)
			if passedThreshold == True:
				outputSignals[i] = numpy.add(outputSignals[i], signalSum)
		      
		i += 1
	return outputSignals
		
	
def maxXcorSum (startingSignal, signals):
  
	threshold = 0.1
	
	if len(signals) == 0:
		 return numpy.zeros(signals[0].shape[0]), signals, False
			
	for i in range(len(signals)):
				
		if i == 0:
			outputSignal = startingSignal
			maxXcor = correlation(outputSignal, signals[0])
			maxXcorSignalIndex = 0
		else:
			cor = correlation(outputSignal, signals[i])
			if cor > maxXcor:
				maxXcor = cor
				maxXcorSignalIndex = i
			
	if maxXcor > threshold:
		outputSignal = numpy.add(outputSignal, maxXcorSignalIndex)
		signals.pop(maxXcorSignalIndex)
		return outputSignal, signals, True
	else:
		return numpy.zeros(signals[0].shape[0]), signals, False
	      
	      
def correlation (signal_1, signal_2):
  
	cor = scipy.stats.pearsonr(signal_1, signal_2)[0]
	print cor
	return cor
  
  
  
  
  
  
  
  
  





