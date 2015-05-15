import pyfasst.audioModel as am
import Mixer

filename = 'br_overwatch05_noise.wav'

model = am.MultiChanNMFConv(audio=filename, nbComps=4, nbNMFComps=32, spatial_rank=1, verbose=1, iter_num=75)

model.makeItConvolutive()

#model.initializeConvParams(initMethod='demix')

model.estim_param_a_post_model()

model.separate_spat_comps(dir_results='output/')

