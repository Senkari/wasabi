
#this script demonstrates the use of Mixer-module

import scipy.io.wavfile as wav
import numpy

import Mixer


rate, dataList = Mixer.readFiles(["hl2_01.wav", "hl2_02.wav"])

data = Mixer.mixInputs(dataList);
data = Mixer.addReverb(data, 5000, 0.2, 3)
data += numpy.random.normal(0, 2000, data.shape[0]) 	#add some noise

wav.write("mix", rate, data) 
