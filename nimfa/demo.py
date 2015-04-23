import scipy.io.wavfile as wav
from scipy.fftpack import *
from scipy.signal import *
from pylab import *
import numpy
import nimfa
import os

import Mixer


rate, dataList, maxDataLength = Mixer.readFiles(["hl2_01.wav", "hl2_02.wav"])

data = Mixer.mixInputs(dataList, maxDataLength);
data = Mixer.addReverb(data, 5000, 0.2, 3)
data += numpy.random.normal(0, 2000, data.shape[0]) 	#add some noise

if not os.path.exists("output"):
    os.makedirs("output")
    
wav.write("output/mix", rate, data) 



##http://dsp.stackexchange.com/questions/4697/time-frequency-analysis-of-non-sinusoidal-periodic-signals/4700#4700
##http://www.cs.tut.fi/sgn/arg/music/tuomasv/virtanen_taslp2007.pdf


##Default window function for specgram is Hanning;
##w(n) = 0.5*(1-cos(2*pi*n/(N-1)))

##Window size and type for chopping the signal
winsize = 256
win = numpy.hanning(winsize)

periodograms = []

##Loop parameters, no need to adjust
loop = 1
l = 0

##Construct spectrogram data
while(loop==1):
	chunk = []
	for i in range(winsize):
		chunk.append(data[l])
		l+=1
		if l == len(data)-1:
			loop = 0
			if i != winsize-1:
				padding = numpy.zeros(winsize-i-1)
				chunk += list(padding)
				break
	##Overlap index back for a half-window
	l -= int(round(winsize/2.0)) + 1
	
	periodograms.append(fft(chunk*win))
	
##Store original phase data
angles = angle(periodograms)

spectros = abs(numpy.asarray(periodograms))


##TODO: normalization
#f, Pxx = welch(data, noverlap=128)
#spectros = spectros / Pxx

##Reconstruction:
##http://dsp.stackexchange.com/questions/9877/reconstruction-of-audio-signal-from-spectrogram
##http://dsp.stackexchange.com/questions/3406/reconstruction-of-audio-signal-from-its-absolute-spectrogram/3410#3410
##http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.306.7858&rep=rep1&type=pdf
##http://eeweb.poly.edu/iselesni/EL713/STFT/stft_inverse.pdf
##http://isdl.ee.washington.edu/people/stevenschimmel/sphsc503/files/handout5.pdf
##http://dsp.stackexchange.com/questions/10743/generating-spectrograms-in-python-with-less-noise

### Different nmf-approaches (http://nimfa.biolab.si)
##Adjust rank according to number of components to be extracted, try different algs and parameters

#nmf = nimfa.Nmf(spectros, max_iter=1000, rank=6, update='euclidean', objective='fro')

#nmf = nimfa.Snmf(spectros, seed="random_vcol", rank=1*winsize, max_iter=5, version='l', eta=1., beta=1e-4, i_conv=10, w_min_change=0) #ValueError: operands could not be broadcast together with shapes (256,300) (256,301)

#nmf = nimfa.Lfnmf(spectros, seed=None, W=np.random.rand(spectros.shape[0], 1*winsize), H=np.random.rand(1*winsize, spectros.shape[1]), rank=1*winsize, max_iter=20, alpha=0.01)

#nmf = nimfa.Lsnmf(spectros, seed="random_vcol", rank=1*winsize, max_iter=12, sub_iter=10, inner_sub_iter=10, beta=0.1)

###




rank = 2 #needed for printing progress (optional)

nmf = nimfa.Bd(spectros, seed="random_c", rank=rank, max_iter=100, alpha=np.zeros((spectros.shape[0], 10)), beta=np.zeros((10, spectros.shape[1])), theta=.0, k=.0, sigma=1., skip=100, stride=1, n_w=np.zeros((rank, 1)), n_h=np.zeros((rank, 1)), n_sigma=False)



nmf_fit = nmf()
W = nmf_fit.basis()
H = nmf_fit.coef()

l = 0
sources = []
recovered = []
source = numpy.asarray([])

##Extracted components to spectral form
for i in range(W.shape[1]):
	sources.append(W[:,i]*H[i])
  
##Spectrograms back to sound
for i in range(len(sources)):
	sources[i] = numpy.asarray(sources[i])
	
	##Apply original phase data to the separated amplitudes
	sources[i] = sources[i]*numpy.e**(1j * angles)
	
	##Process each window
	for j in range(len(sources[i])):
		##Inverse Fourier
		chunk = ifft(sources[i][j])
		
		##Window back
		chunk = chunk*win
		
		if j==0:
			source = chunk
			l = chunk.shape[0] - int(winsize/2)
		else:
			##Handle overlapping
			chunk = numpy.concatenate((numpy.zeros(l), chunk))
			source = numpy.concatenate((source, zeros(winsize/2)))
			source += chunk
			l += int(winsize/2)
	
	data = Mixer.normalise(numpy.asarray(source).real)
	name = "output/recovered_"+str(i+1)+".wav"
	wav.write(name, rate, data)
	
	print str(i + 1) + "/" + str(rank) + " recovered"
	
	source = numpy.asarray([])
	l=0





















