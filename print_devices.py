"""List device names"""

from pygame._sdl2 import get_num_audio_devices, get_audio_device_name #Get playback device names
from pygame import mixer #Playing sound

if __name__ == '__main__':
    mixer.init()
    print('DEVICES: ')
    print([get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))])
    mixer.quit()