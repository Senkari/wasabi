import scipy.io.wavfile as wav
import pyfasst.audioModel as am
import os
import numpy
import Mixer

file1="input/al_anotherpet.wav"
file2="input/br_overwatch05.wav"
file3="input/mo_extrahelp05.wav"
file4="input/monk_rant01.wav"
file5="input/hutama_request.wav"
file6="input/oda_nobunaga_intro.wav"
f = 0
for i in range(15):
    filelist = []
    if i == 0:
        filelist.append(file1)
        filelist.append(file2)
        comboString = "Anotherpet_Overwatch"
    elif i == 1:
        filelist.append(file1)
        filelist.append(file3)
        comboString = "Anotherpet_Extrahelp"
    elif i == 2:
        filelist.append(file1)
        filelist.append(file4)
        comboString = "Anotherpet_Rant"
    elif i == 3:
        filelist.append(file1)
        filelist.append(file5)
        comboString = "Anotherpet_Hutama"
    elif i == 4:
        filelist.append(file1)
        filelist.append(file6)
        comboString = "Anotherpet_Nobunaga"
    elif i == 5:
        filelist.append(file2)
        filelist.append(file3)
        comboString = "Overwatch_Extrahelp"
    elif i == 6:
        filelist.append(file2)
        filelist.append(file4)
        comboString = "Overwatch_Rant"
    elif i == 7:
        filelist.append(file2)
        filelist.append(file5)
        comboString = "Overwatch_Hutama"
    elif i == 8:
        filelist.append(file2)
        filelist.append(file6)
        comboString = "Overwatch_Nobunaga"
    elif i == 9:
        filelist.append(file3)
        filelist.append(file4)
        comboString = "Extrahelp_Rant"
    elif i == 10:
        filelist.append(file3)
        filelist.append(file5)
        comboString = "Extrahelp_Hutama"
    elif i == 11:
        filelist.append(file3)
        filelist.append(file6)
        comboString = "Extrahelp_Nobunaga"
    elif i == 12:
        filelist.append(file4)
        filelist.append(file5)
        comboString = "Rant_Hutama"
    elif i == 13:
        filelist.append(file4)
        filelist.append(file6)
        comboString = "Rant_Nobunaga"
    elif i == 14:
        filelist.append(file5)
        filelist.append(file6)
        comboString = "Hutama_Nobunaga"
    else:
        print "Erroneus value i. Exiting..."
        sys.exit()
    print "List filelist contains: ", filelist
    rate, dataList, maxDataLength = Mixer.readFiles(filelist)

    for j in range(-5, 6):

        data = Mixer.mixInputs(dataList[0], dataList[1], maxDataLength, j)
        data = Mixer.normalise(data)

        for k in range(-10, 7):

            dirName = str(j)+"dBmix_"+str(k)+"dBnoise"
            if not os.path.exists("output/"+dirName):
                os.makedirs("output/"+dirName)
            if not os.path.exists("output/"+dirName+"/"+comboString):
                os.makedirs("output/"+dirName+"/"+comboString)

            if k == 6:
                comps = 2
            else:
                data = Mixer.addNormalNoise(data, k)
                comps = 4

            wav.write("input/mix.wav", rate, numpy.int16(data.T * 32767))
            model = am.MultiChanNMFConv("input/mix.wav", nbComps=comps, nbNMFComps=32, spatial_rank=1, verbose=1, iter_num=50)
            model.makeItConvolutive()
            model.estim_param_a_post_model()
            model.separate_spat_comps(dir_results="output/"+dirName+"/"+comboString)
            f += 1
print f
