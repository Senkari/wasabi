import pyfasst.audioModel as am
filename = 'mix.wav'

model = am.MultiChanNMFConv(audio=filename, nbComps=2, nbNMFComps=32, spatial_rank=1, verbose=1, iter_num=200)

model.makeItConvolutive()

#model.initializeConvParams(initMethod='demix')

model.estim_param_a_post_model()

model.separate_spat_comps(dir_results='output/')

