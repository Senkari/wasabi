
#this script demonstrates the use of Mixer-module

import scipy.io.wavfile as wav
import numpy
import os

import Mixer


rate, dataList, maxDataLength = Mixer.readFiles(["hl2_01.wav", "hl2_02.wav"])

data = Mixer.mixInputs(dataList, maxDataLength);
data = Mixer.addReverb(data, 5000, 0.2, 3)
data += numpy.random.normal(0, 2000, data.shape[0]) 	#add some noise
data = Mixer.normalise(data)

if not os.path.exists("MixerDemooOutput"):
    os.makedirs("MixerDemooOutput")
    
wav.write("MixerDemooOutput/mix", rate, data) 
