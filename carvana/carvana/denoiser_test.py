import keras
import argparse
import time
import tensorflow as tf
from math import ceil
from keras.backend.tensorflow_backend import set_session
from utils import *
from config import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import sys


def create_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=float, default=1)
    parser.add_argument('--gpus', type=str, default='cpu')
    return parser.parse_args()

on_amax = True

img_dir = os.path.join(os.path.expanduser('~'), 'Desktop/MarsWorkSpace/Denoising_AutoEncoders/carvana/test')

if on_amax:
    img_dir = '/Users/mohitakhakharia/Desktop/MarsWorkSpace/Denoising_AutoEncoders/carvana/test'
total_fns = [os.path.splitext(os.path.basename(x))[0] for x in glob.glob(os.path.join(img_dir, '*.jpg'))]
fn_dict = {fn: [os.path.join(img_dir, fn + '.jpg')] for fn in total_fns}
print (".....fn_dict.....")
print (fn_dict)

steps = ceil(len(total_fns)/BATCH_SIZE)


if __name__ == "__main__":
    args = create_args()
    # configure gpu
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = args.gpu
    config.gpu_options.visible_device_list = args.gpus
    set_session(tf.Session(config=config))

    print("choose from...")
    models = glob.glob('experiment/model*')
    for i,model in enumerate(models):
        print("{}-{}".format(i, model))
    i = int(input("choose pred model: "))
    print("selected {}...displaying details...".format(models[i]))

    submodels = glob.glob(os.path.join(models[i], '*.hdf5'))
    for j, submodel in enumerate(submodels):
        print("{}-{}".format(j, submodel))
    i1 = int(input("choose pred model: "))
    if i1 in list(range(len(submodels))):
        submodel = submodels[i1]
    else:
        submodel = os.path.join(models[i], 'best_model.hdf5')

    model = keras.models.load_model(submodel, custom_objects={'dice_coef':dice_coef, 'bce_dc_loss':bce_dc_loss})
    print("model loaded for {}...".format(submodel))

    print ("total_fns",total_fns)
    print ("fn_dict",fn_dict)
    print ("TARGET_SIZE",TARGET_SIZE)
    print ("BATCH_SIZE",BATCH_SIZE)
    test_gen = DataIterator(fns=total_fns, fn_dict=fn_dict, target_size=TARGET_SIZE, test=True, batch_size=BATCH_SIZE)
    

    print("predicting...")
    now = time.time()
    pred = model.predict_generator(test_gen, steps=steps, verbose=1, workers=3)

    print("DEBUG: ", type(pred))
    print("DEBUG: ", np.max(pred.flatten()))
    print("DEBUG: ", np.min(pred.flatten()))
    print("DEBUG: ", pred.shape)
    print("DEBUG - pred[1]: ", pred[1])
    np.save('image_cuts.npy',pred)
    print("DEBUG: prediction takes %2f to proceed..." % (time.time()-now))