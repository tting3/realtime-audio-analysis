
# The purpose of this file is to enable realtime
# input from the microphone.

BLOCK_TIME = 0.1                        # Size of input block in seconds
RATE = 44100                            # Sampling rate in Hertz
CHANNELS = 2                            # number of input channels
FRAME_PER_BLOCK = int(BLOCK_TIME*RATE)  # number of samples per block
NORMALIZE_VALUE = 32768                 # 2^15 (assume pyaudio.paInt16)

import pyaudio
import struct
import Queue
import threading
import time
import wave

class AudioIN():
    
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
    a = AudioIN()
    a.start_stream()
    
    for i in range(10):
        time.sleep(0.1)

    a.stop_stream()
    print "done stream"
    a.terminate()

    print a.getData()



if __name__ == "__main__":
    main()

