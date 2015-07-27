__author__ = 'hetianyi'
"""
##
    @input: Input signal after STFT form
    @dftsz: Size of Each frame to be taken with DFT/FFT .. Use Even Number
    @hopsz: The size of each un-overlapped part
    @window: The window to be used, default to be no window, need to be the same size as dftsz
##
"""

import numpy as np
import pylab as pl
from overlapadd import overlapadd


def ISTFT(input,dftsz,hopsz,window):
    # Get frame number
    #framenum = np.size(input,1)

    dummat = np.conj(input)

    # If Even dftsz
    dummat = dummat[-2::-1,:] # Flip the matrix so to append onto input
    dummat = np.concatenate((input,dummat),axis = 0)

    # If Odd dftsz, do not want to consider now
    # dummat = dummat[3::-1,:]


    # How to concatinate?


    dummat = np.fft.irfft(dummat,dftsz,0)

    # Overlap-Add
    output = overlapadd(dummat, dftsz, hopsz, window)

    return output
