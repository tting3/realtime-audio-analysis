
# The purpose of this file is to enable realtime
# input from the microphone.

WINDOW_SIZE = 4000                      # Number of data per frame
HOP_SIZE = int(WINDOW_SIZE*0.75)        # allows overlap
BLOCK_TIME = 0.01                       # Size of input block in seconds
RATE = 44100                            # Sampling rate in Hertz
CHANNELS = 1                            # number of input channels
FRAME_PER_BLOCK = int(BLOCK_TIME*RATE)  # number of samples per block
NORMALIZE_VALUE = 32768                 # 2^15 (assume pyaudio.paInt16)


import pyaudio
import struct
import Queue
import threading
import time
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# This class is the module that will be drawing the data
# NOTE: it does not process any data, but simply obtain
# the data that is to be plotted
class AnimationUnit():
    
    def __init__(self, data_source):
        #self.fig, self.ax = plt.subplots()
       
        self.xaxis = [x for x in range(WINDOW_SIZE/2)] 
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, WINDOW_SIZE/2), ylim=(0, 10))
        self.line, = self.ax.plot(self.xaxis, [0 for x in range(WINDOW_SIZE/2)])

        # The x-axis will never change; it would make sense
        # to define it now instead of having it updated
        # every iteration

        #self.line, = self.ax.plot(self.xaxis,[x for x in range(0, WINDOW_SIZE/2) ])
        
        # The data_source should have a function called
        # getData() that allows the class to retrieve new
        # data
        self.data_source = data_source     

    
    # This function will be used to update the y_axis
    def update(self, dummy):
        data = self.data_source.getData()[0:WINDOW_SIZE/2]
        self.line.set_ydata(data)
        
        #self.ax.clear()
        #self.ax.plot(self.xaxis, data)
        return self.line,

    # This function will start the animation
    def draw(self):
        ani = animation.FuncAnimation(self.fig, self.update, interval=50)
        # the show method is a blocking function; hence one would need to
        # utilize the threading module to allow further execution
        plt.show()


# This unit will process raw data from audio input
# and provide data to the drawing unit.
class ProcessUnit():

    def __init__(self, data_source):
        # The data source should have a funciton
        # called getData() that allows the class
        # to retrieve new data
        self.data_source = data_source
        
        # This queue contains the data that has
        # been processed.
        self.donePackage = Queue.Queue()
   
        self.data_buffer = [] 

    # Provides the processed data to caller
    def getData(self):
        return self.donePackage.get()

    # This function collect WINDOW_SIZE
    # amount of data, process it, and
    # put the result in donePackage
    def process(self):
        while(True):
            currData = self.data_buffer
            currSize = len(currData)
            while(currSize < WINDOW_SIZE):
                newData = self.data_source.getData()
                currData += newData
                currSize += FRAME_PER_BLOCK
            
            package = currData[0:WINDOW_SIZE]
            package = self.compute(package)
            self.donePackage.put(package)
            self.data_buffer = currData[HOP_SIZE:]

    def compute(self, data):
        return abs(numpy.fft.fft(data))

# This class is responsible for acquiring
# raw data from the microphone
class InputUnit():
    
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.default_input_devInfo = self.p.get_default_input_device_info()
        self.print_Macros()
        self.stream = self.p.open(
                                    format=pyaudio.paInt16, 
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    frames_per_buffer=FRAME_PER_BLOCK,
                                    stream_callback=self.listen
                                 )
        self.stream.start_stream()
        self.dataQueue = Queue.Queue()
        self.print_devInfo()

    # starts audio input; data will be put in dataQueue
    def start_stream(self):
        self.stream.start_stream()

    # stop audio input; should be able to be restart
    def stop_stream(self):
        self.stream.stop_stream()

    
    # Print out the information of the default input
    # device. User may use this function to ensure
    # corresponding MACROs have been defined correctly
    def print_devInfo(self):
        print "========== Default input device info =========="
        for key in self.default_input_devInfo:
            print key, ":", self.default_input_devInfo[key]
        print "==============================================="

    def print_Macros(self):
        print "========== MACROS =========="
        print "CHANNELS:", CHANNELS
        print "SAMPLING RATE:", RATE
        print "BLOCK_TIME:", BLOCK_TIME
        print ""

    # Callback function; simply puts input data
    # in the data queue when data is ready
    def listen(self, in_data, frame_count, time_info, status):
        self.dataQueue.put(in_data)
        return ('', pyaudio.paContinue)

    # Get data from the queue; the return object
    # would be the normalized list from the string
    # unpacked; Note that this call will block if
    # there is nothing in the queue
    def getData(self):
        data_block = self.dataQueue.get()
        fmt = "%dh" % (len(data_block)/2)
        unpacked_data = struct.unpack(fmt, data_block)
        data_list = []
        for sample in unpacked_data:
            data_list.append(float(sample)/NORMALIZE_VALUE)
        
        return  data_list

    # Call when AudioIn is not needed anymore
    def terminate(self):
        self.stream.close()
        self.p.terminate()

def main():
    microphone = InputUnit()
    processor = ProcessUnit(microphone)
    drawer = AnimationUnit(processor)

    processor_thread = threading.Thread(target=processor.process)
    processor_thread.daemon = True

    # These calls does not block
    microphone.start_stream()
    processor_thread.start()


    drawer.draw()

    """ 
    for i in range(100):
        if(i %10 ==0):
            print "================="
        time.sleep(0.1)
    """ 

    microphone.stop_stream()
    microphone.terminate()



if __name__ == "__main__":
    main()

