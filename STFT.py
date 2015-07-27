import numpy as np
import pylab as pl
from vectorize2d import vectorize2d


"""
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
##
"""

def STFT(input,dftsz,hopsz,window,graph = True):
    channel = input.ndim

    if channel > 1:
        input = input[:,0] # if multi-channel, take the first channel
    else:
        input = input



    mat2d = vectorize2d(input,dftsz,hopsz,window)
    mat2d = np.fft.fft(mat2d,dftsz,0)

    # If even dftsz
    if dftsz % 2 == 0:
        cutpt = dftsz / 2 + 1

    # If odd dftsz
    else:
        cutpt = np.ceil(dftsz/2) + 2


    output = mat2d[:cutpt,:]
    output = output[::-1]

    if graph == True:
        imag = np.log(abs(output))
        #imag =  (abs(test1)) ** 0.4
        pl.matshow(imag)
        pl.show()


    return output
##
#STFT()







