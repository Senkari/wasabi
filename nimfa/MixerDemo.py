
#this script demonstrates the use of Mixer-module

import scipy.io.wavfile as wav
import numpy
import os

import Mixer


rate, dataList, maxDataLength = Mixer.readFiles(["input/br_overwatch05.wav", "input/al_anotherpet.wav"])

data, dataList[0], dataList[1] = Mixer.mixInputs(dataList[0], dataList[1], maxDataLength, -1);
data = Mixer.addNormalNoise (data, -5)


if not os.path.exists("MixerDemoOutput"):
    os.makedirs("MixerDemoOutput")
    
    
wav.write("MixerDemoOutput/mix.wav", rate, numpy.int16(data.T * 32767))

data = Mixer.stereoToMono("MixerDemoOutput/mix.wav")

wav.write("MixerDemoOutput/mix2.wav", rate, numpy.int16(data.T * 32767))

