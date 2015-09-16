__author__ = 'hetianyi'
import numpy as np
import scipy as sp
import pylab as pl
# This File Extract the following features and output a vector
#
# Cepstrum Coeffs. with Mel-Frequency Warpping
# Zero Crossing Rate
# Total Energy

def features(x,cepssize,banksize):
    length = len(x)
    # MFCC
    x_dft = np.fft.fft(x)
    t_bank = triangular_bank(banksize,length)
    x_dft_mel = t_bank * x_dft
    x_mfcc = np.fft.ifft(np.log(abs(x_dft_mel)))
    x_mfcc = x_mfcc[0:cepssize-1]

    # Zero-Xing
    x1 = [0] * (length + 1)
    x2 = x1
    x1[0:length - 1] = x
    x2[1:length] = x
    xt = np.dot(x1, x2)
    rate = round(len(np.where( x <= 0 ))/2)

    # Energy
    energy = np.linalg.norm(x_dft)

    # Features
    feature = [0] * (cepssize+2)
    feature[0:cepssize-1] = x_mfcc
    feature[cepssize] = rate
    feature[cepssize+1] = energy

    return feature

def triangular_bank(banksize,dftsize):

     #hz2mel = @( hz )( 1127*log(1+hz/700) );     % Hertz to mel warping function
     #mel2hz = @( mel )( 700*exp(mel/1127)-700 ); % mel to Hertz warping function

     # Find the center point of each triangle
     endpt = np.log(1+44100/700)*1127
     centerpt = np.linspace(0,endpt,banksize+2)
     centerpt_hz = np.round(700 * (np.exp(centerpt/1127)-1) / 44100 * dftsize)
     # Make the Matrix
     ret = np.zeros((banksize,dftsize))
     for i in range(1, banksize):
        #print i
        ret[i,centerpt_hz[i-1]:centerpt_hz[i+1]+1] = triang(centerpt_hz[i+1]-centerpt_hz[i-1] + 1)
     dum = triang(centerpt_hz[1]*2)
     ret[0,0:int(centerpt_hz[1]) - 1] = dum[int(centerpt_hz[1]): int(centerpt_hz[1]*2) - 1]
     return ret

def triang(size):
    ret = [0] * size
    # first half
    topp = int(np.floor(size/2))

    if (size%2 == 0):
        for i in range(0, topp):
            ret[i] = 1.0 / (topp+0.5) * (i)
        ret[-1:topp-1:-1] = ret[0:topp]
    else:
        for i in range(0, topp):
            ret[i] = 1.0 / (topp) * (i)
        ret[topp] = 1
        ret[-1:topp:-1] = ret[0:topp]
    return ret

