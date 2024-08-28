import time
# test nava library and mp3
from nava import play, stop

import os
import sys
def resource_path(relative_path):

    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    toReturn = os.path.join(base_path, relative_path)
    print(f"toReturn: {toReturn}")
    return toReturn

audio_path = resource_path("assets/end_sfx.mp3")

sound_id = play(audio_path, async_mode=True, loop=False)
# this allows asyncrhonous audio playing
time.sleep(4)
stop(sound_id)

