__author__ = 'hetianyi'
import numpy as np


def overlapadd(input, windowsz, hopsz, window):

    #if all(window) == 1:
    #    window = np.ones((windowsz,1))

    framenum = np.size(input, 1)

    output = np.zeros(((framenum) * hopsz + windowsz,))

    counter = 0
    while counter < framenum:
        output[counter * hopsz : counter * hopsz + windowsz] = input[:, counter] * window
        counter += 1

    return output
