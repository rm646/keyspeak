import queue
import keyboard  
import os
from multiprocessing import Process
import threading
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from gtts import gTTS
from pygame._sdl2 import get_num_audio_devices, get_audio_device_name #Get playback device names
from pygame import mixer #Playing sound

SPEAKER_DEVICE_NAME = 'Headphones (High Definition Audio Device)'
MIC_DEVICE_NAME = 'CABLE Input (VB-Audio Virtual Cable)'


def play_file_through_device(filename: str, devicename: str, temp: bool) -> None:
    mixer.init(devicename=devicename) #Initialize it with the correct device
    mixer.music.load(filename) #Load the mp3
    mixer.music.play() #Play it
    while mixer.music.get_busy():
        time.sleep(0.1)
    if temp:
        mixer.quit()
        os.remove(filename)

def play_file(filename: str, temp=False) -> None:
    """play a given mp3 file, destroying afterwards if desired"""
    # mic_input_thread = threading.Thread(
    mic_input_thread = Process(
        target=play_file_through_device,
        args=(filename, MIC_DEVICE_NAME, temp),
    )
    speaker_input_thread = Process(
        target=play_file_through_device,
        args=(filename, SPEAKER_DEVICE_NAME, temp),
    )
    mic_input_thread.start()
    speaker_input_thread.start()

def generate_from_input():
    """generate a sound file from keyboard input,
    play it, then delete that file"""
    rec = keyboard.record(until="enter")
    text = "".join([r.name if r.name != 'space' else ' ' for r in rec if r.event_type == "down" and r.name != 'enter'])
    print(text)
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("custom.mp3")
    play_file("custom.mp3", temp=True)

ACTION_KEYS = {  # scan code: function
    71 : (lambda: play_file('northwest.mp3')),  # numpad 7
    72 : (lambda: play_file('north.mp3')),  # numpad 8
    73 : (lambda: play_file('northeast.mp3')),  # numpad 9
    75 : (lambda: play_file('west.mp3')),  # numpad 4
    76 : (lambda: play_file('danger_close.mp3')),  # numpad 5
    77 : (lambda: play_file('east.mp3')),  # numpad 6
    79 : (lambda: play_file('southwest.mp3')),  # numpad 1
    80 : (lambda: play_file('south.mp3')),  # numpad 2
    81 : (lambda: play_file('southeast.mp3')),  # numpad 3
    53 : (lambda: play_file('bollocks.mp3')),  # /
    55 : (lambda: play_file('footsteps.mp3')),  # *
    82 : (lambda: play_file('got_one.mp3')),  # numpad 0
    83 : (lambda: play_file('haha.mp3')),  # numpad del
    74 : (lambda: generate_from_input()),  # numpad minus
}

def app_main_loop():
    # Create another thread that monitors the keyboard
    input_queue = queue.Queue()
    kb_input_thread = threading.Thread(target=_check_pressed, args=(input_queue,))
    kb_input_thread.daemon = True
    kb_input_thread.start()
    
    # Main logic loop
    run_active = True
    while True:
        if not input_queue.empty():
            if run_active:
                top = input_queue.get()
                if top == "esc":
                    run_active = False
                    print("Esc pressed, stopping")
                    break
                for key in ACTION_KEYS:
                    if top == key:
                        ACTION_KEYS[key]()
        time.sleep(0.1)  # seconds

def _check_pressed(input_queue: queue.Queue) -> None:
    while True:
        if keyboard.is_pressed('esc'):
            input_queue.put("esc")
        for key in ACTION_KEYS:
            if keyboard.is_pressed(key):
                input_queue.put(key)
        time.sleep(0.1) # seconds

if __name__ == "__main__":
    app_main_loop()