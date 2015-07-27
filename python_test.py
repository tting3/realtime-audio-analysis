import numpy as np
import pylab as pl
import scipy.io.wavfile as siow
from STFT import STFT
from ISTFT import ISTFT
dftsz = 512
hopsz = 128
window = np.hamming(dftsz)
filename = '80s.wav'
(Fs,input) = siow.read(filename)

fig = pl.figure()
#ax1 = fig.add_subplot(1,1,1)
output = STFT(input,dftsz,hopsz,window,False)
soundout = ISTFT(output,dftsz,hopsz,window)
pl.plot(soundout)
pl.show()

def draw(dftsz,hopsz,window,input):

    imag = np.log(abs(output))
    #imag =  (abs(test1)) ** 0.4
    axe = pl.matshow(imag)
    return axe


fig = draw(dftsz,hopsz,window,input)
pl.show(fig)
"""
#pl.plot(test)
#pl.show()
print np.size(test1,0)
#test = test[:,0]

#timel = len(test)/Fs
#print len(test)/hopsz

#test = STFT(test,dftsz,hopsz,window)

imag = np.log(abs(test1))
#imag =  (abs(test1)) ** 0.4
pl.matshow(imag)
pl.show()
"""