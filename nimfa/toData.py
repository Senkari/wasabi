import scipy.io.wavfile as siow
import numpy

fileIn = "file.wav"
rate, data = siow.read(fileIn)
print data
