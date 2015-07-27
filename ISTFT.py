__author__ = 'hetianyi'


import numpy as np
import pylab as pl

def STFT(input,dftsz,hopsz,window):
    # Get frame number
    framenum = np.size(input,1)

    dummat = np.conj(input)

    # If Even dftsz
    dummat = dummat[2::-1,:]

    # If Odd dftsz
    dummat = dummat[3::-1,:]


    # How to concatinate?


    dummat = np.fft.ifft(dummat)

    # Overlap-Add
    output = overlapadd(input, dftsz, hopsz, window)
