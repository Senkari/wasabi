import pyfasst.audioModel as am
import os
import Mixer

file1="input/al_anotherpet.wav"
file2="input/br_overwatch05.wav"
file3="input/mo_extrahelp05.wav"
file4="input/monk_rant01.wav"
f = 0
for i in range(6):

    filelist = []
    if i == 0:
        filelist.append(file1)
        filelist.append(file2)
    elif i == 1:
        filelist.append(file1)
        filelist.append(file3)
    elif i == 2:
        filelist.append(file1)
        filelist.append(file4)
    elif i == 3:
        filelist.append(file2)
        filelist.append(file3)
    elif i == 4:
        filelist.append(file2)
        filelist.append(file4)
    elif i == 5:
        filelist.append(file3)
        filelist.append(file4)
    else:
        print "Erroneus value i. Exiting..."
        sys.exit()
    print "List filelist contains: ", filelist
    rate, dataList, maxDataLength = Mixer.readFiles(filelist)

    for j in range(-5, 6):

        data = Mixer.mixInputs(dataList[0], dataList[1], maxDataLength, 0.9)

        for k in range(20):

            #ADD NOISE HERE
            if not os.path.exists(str(k)):
                os.makedirs(str(k))
            data = Mixer.normalise(data)
            wav.write("input/mix.wav", rate, numpy.int16(data.T * 32767))
            model = am.MultiChanNMFConv(audio=filename, nbComps=2, nbNMFComps=32, spatial_rank=1, verbose=1, iter_num=200)
            model.makeItConvolutive()
            model.estim_param_a_post_model()
            model.separate_spat_comps(dir_results='output/'+str(k))
            f += 1

print f
