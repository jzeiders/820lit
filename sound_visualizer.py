# Author: Samuel Resendez

import pyaudio
import time
import numpy as np
import math

from matplotlib import pyplot as plt


CHANNELS = 1
RATE = 8000
CHUNK = 130
# 60 per second


p = pyaudio.PyAudio()
curr_average = 0


def sigmoid(x):
    return int(100 / (1 + 8 * math.exp(-0.0003 * x)))


def callback(in_data, frame_count, time_info, flag):
    global curr_average
    audio_data = np.fromstring(in_data, dtype=np.int16)

    print(sigmoid(max(audio_data)))

    # do processing here

    return (audio_data, pyaudio.paContinue)


def main():
    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer=CHUNK,
                    input=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(5)
        stream.stop_stream()

    stream.close()

    p.terminate()

if __name__ == "__main__":
    main()