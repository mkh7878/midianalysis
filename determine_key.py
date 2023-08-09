import mido
import intervals
import time
from playsinewaves import play_sound
from timestamps import TimeTracker
import threading
import os

time_tracker = TimeTracker()
captured_notes = []

# Tells us if there are any midi devices attached, and if so, what they are called
# My midi keybaord is called "MPK mini 3"
def findMidiDevice():
    mido.set_backend('mido.backends.rtmidi')
    # mido.set_backend('mido.backends.portmidi')
    input_names = mido.get_input_names()
    print("Available MIDI input devices:")
    for name in input_names:
        print(name)


if __name__ == '__main__':
    findMidiDevice()

def start_timer():
    return time.time()

def musicmusic():
    # start the timer
    start_time = start_timer()

    # Get the name of the MIDI input device (your MIDI keyboard)
    input_name = mido.get_input_names()[0]  # Assuming your MIDI keyboard is the first device in the list

    # Open the MIDI input device
    with mido.open_input(input_name) as port:
        print(f"Connected to {input_name}...")

        # Infinite loop to keep capturing MIDI messages
        while True:
            for message in port.iter_pending():

                # when a note is played on the midi keyboard
                if message.type == 'note_on':

                    # the current note value in relation to 0
                    current_note = message.note % 12

                    # add to the list of captured notes
                    captured_notes.append(current_note)
                    print(captured_notes)

                    frequency = 2 ** ((message.note - 69) / 12) * 440
                    duration = 0.05  # Duration in seconds (you can adjust this)
                    play_sound(frequency, duration)


                # elif message.type == 'note_off':
                # average_bpm = time_tracker.get_bpm()
                # print(average_bpm)
                # in_between_times = time.time()
                # in_between_time.append(in_between_times * 1000)
                # print (in_between_time)

def determine_key():
    time.sleep(10)
    #captured_notes is a list of all the notes caputured
    for idx in captured_notes:
        #get the note being played and add it to the interval_recurrance
        if captured_notes[idx] in intervals.interval_recurrance:
            intervals.interval_recurrance[idx] += 1

    print(intervals.interval_recurrance)

if __name__ == '__main__':
    # Start the music function in a separate thread
    music_thread = threading.Thread(target=musicmusic)
    music_thread.start()

    # Start the determine_key function in a separate thread
    key_thread = threading.Thread(target=determine_key)
    key_thread.start()


