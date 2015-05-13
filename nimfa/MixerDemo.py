
#this script demonstrates the use of Mixer-module

import scipy.io.wavfile as wav
import numpy
import os

import Mixer


rate, dataList, maxDataLength = Mixer.readFiles(["input/hl2_01.wav", "input/hl2_02.wav"])

dataList[0] = Mixer.addReverb(dataList[0], 5000, 0.2, 3)
dataList[1] = Mixer.addReverb(dataList[1], 5000, 0.2, 3)

#dataList[0] = Mixer.normalise(dataList[0])
#dataList[1] = Mixer.normalise(dataList[1])

data = Mixer.mixInputs(dataList[0], dataList[1], maxDataLength, 0.9);

#data += numpy.random.normal(0, 2000, data.shape[0]) 	#add some noise

data = Mixer.normalise(data)

if not os.path.exists("MixerDemoOutput"):
    os.makedirs("MixerDemoOutput")
    
wav.write("MixerDemoOutput/mix.wav", rate, numpy.int16(data.T * 32767)) 
