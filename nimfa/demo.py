import scipy.io.wavfile as wavi
import numpy
import nimfa

fileIn = "wasabidemo.wav"				#"classical_5db_1.wav"
rate, data = wavi.read(fileIn)
minNum = data.min()
if(minNum < 0):
    minNum *= -2
else:
    minNum = 0

sumData = numpy.sum([data, minNum])
numpy.savetxt("sumData", sumData)
nmf = nimfa.Nmf(sumData, max_iter=10, rank=2, update='euclidean', objective='fro')
nmf_fit = nmf()

W = nmf_fit.basis()
#print W[:,0]
trueW = numpy.sum([W, -minNum])

#Record columns according to rank (for loop would be nicer)
wavi.write("wasaW1.wav", rate, trueW[:,0])
wavi.write("wasaW2.wav", rate, trueW[:,1])
#wavi.write("wasaW3.wav", rate, trueW[:,2])
#wavi.write("wasaW4.wav", rate, trueW[:,3])

H = nmf_fit.coef()
#print H
trueH = numpy.sum([H, -minNum])
wavi.write("wasaH.wav", rate, trueH)
