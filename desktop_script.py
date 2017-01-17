from visualizer import Visualizer
from pattern import Pattern
import pattern
import sound_visualizer
import pyaudio
import numpy as np


last_volume = 0
PIXEL_NUM = 240
last_pattern = Pattern()


def patternCreator():
    # return pattern.middleOutRainbowWithFillPatternFromVolume(last_volume, PIXEL_NUM)
    return pattern.middleOutWithEndsRainbowPatternFromVolume(last_volume, PIXEL_NUM, previous=last_pattern, fade=0.95, ending=0.7)


def sound_callback(in_data, frame_count, time_info, flag):
    global last_volume
    audio_data = np.fromstring(in_data, dtype=np.int16)
    # do processing here
    last_volume = sound_visualizer.sigmoid(max(audio_data))

    return (audio_data, pyaudio.paContinue)


def main():
    # visualizer = Visualizer(pattern=pattern.rainbow())
    # visualizer.play(delay=0)
    global last_pattern
    visualizer = Visualizer()
    stream = sound_visualizer.p.open(format=pyaudio.paInt16,
                                     channels=sound_visualizer.CHANNELS,
                                     rate=sound_visualizer.RATE,
                                     frames_per_buffer=sound_visualizer.CHUNK,
                                     input=True,
                                     stream_callback=sound_callback)

    stream.start_stream()

    while stream.is_active():
        new_pattern = patternCreator()
        visualizer.update(new_pattern)
        last_pattern = new_pattern
        visualizer.checkClosure()

    stream.stop_stream()

    stream.close()

    visualizer.p.terminate()


main()
