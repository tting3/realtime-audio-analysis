import numpy as np
#import pylab as lp

def vectorize2d(input,windowsz,hopsz,window):
    leng = len(input)                       # Find the length of the input signal
    framenum = divmod(leng,hopsz)[0] + 1    # Find the frame number
    output = np.zeros([windowsz,framenum])  # Allocate empty array

    counter = 0
    stpt = 0

    while counter < framenum:
        dumvec = input[stpt:min(stpt + windowsz,leng)]                      # Find the signal vector chopped
        output[:len(dumvec),counter]  = dumvec * window[:len(dumvec)]       # Change output zeros to signals chopped with window
        counter += 1                                                        # Counter & startpt increases
        stpt = stpt + hopsz

    # How do I end a While Loop?

    return output

#vectorize2d()



