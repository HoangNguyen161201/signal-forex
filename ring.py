from pydub import AudioSegment
from pydub.playback import play
import threading

def play_music():
    song = AudioSegment.from_mp3("./ring.mp3")
    play(song)

def play_ring():
    thread = threading.Thread(target=play_music)
    thread.start()