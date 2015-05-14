
#this script demonstrates the use of Mixer-module

import scipy.io.wavfile as wav
import numpy
import os

import Mixer


rate, dataList, maxDataLength = Mixer.readFiles(["input/hl2_01.wav", "input/hl2_02.wav"])

data = Mixer.mixInputs(dataList[0], dataList[1], maxDataLength, -1);
data = Mixer.addNormalNoise (data, -10)
data = Mixer.normalise(data)

if not os.path.exists("MixerDemoOutput"):
    os.makedirs("MixerDemoOutput")
    
wav.write("MixerDemoOutput/mix.wav", rate, numpy.int16(data.T * 32767)) 
