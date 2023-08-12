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
# My midi keyboard is called "MPK mini 3"
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

#determining key based on  Krumhansl and Kessler’s (1982) study of tonal organization
#essentially, the key is determined based on which note is played the most
#then, we see if the major or minor 3rd has been played more to determine if it's a minor or magor key
#this is a very simplified version of the theory, and will become more complex as the project grows
def determine_key():
    time.sleep(10)

    #captured_notes is a list of all the notes captured
    for note in range(len(captured_notes)):
        #which note should be updated?
        note_to_tally = captured_notes[note]
        #use note value to index into inthervals_recurrance_list
        #basically, tally up how many times the note has been used.
        intervals.interval_recurrance_list[note_to_tally] += 1

    #holds the number of times a note is played, and changes when one higher is found
    how_many_times = 0
    #variable to hold the index number for whichever note is played the most - this will be the likekly key
    likely_key = 0

    #go through interval_recurrance_list and determine which note has been played the most
    for tally in range(12):
        if intervals.interval_recurrance_list[tally] > how_many_times:
            how_many_times = intervals.interval_recurrance_list[tally]
            likely_key = tally

    likely_key_letter = intervals.notes[likely_key]

    print('the most played note is:', likely_key_letter, 'played', how_many_times, 'times.')

    #According to the Krumhansl and Kessler theory, the key of the piece is likely the note played most
    #and then it's possible to see whether the key is major or minor based on if the major or minor 3rd is
    #played more than the other.
    key_major_third =  (12-(8-likely_key))%12
    #print('major third:', intervals.notes[key_major_third])
    key_minor_third = (12-(9-likely_key))%12
    #print('minor third:', intervals.notes[key_minor_third])


    if intervals.interval_recurrance_list[key_major_third] > intervals.interval_recurrance_list[key_minor_third]:
        print('The music is in the key of', likely_key_letter,'major.')
    elif intervals.interval_recurrance_list[key_minor_third] > intervals.interval_recurrance_list[key_major_third]:
        print('The music is in the key of', likely_key_letter, 'minor.')
    else:
        print('The music is in the key of', likely_key_letter, ', but we can not yet determine if it is major or minor.')

    #eventually we will need to add check points to see if the actual notes being played match up with the key
    #and use other more complex ways of determining key.
    #but this works for now and is pretty fun.
    #I think this should be checked every 30 seconds?

    #print(intervals.interval_recurrance_list)

if __name__ == '__main__':
    # Start the music function in a separate thread
    music_thread = threading.Thread(target=musicmusic)
    music_thread.start()

    # Start the determine_key function in a separate thread
    key_thread = threading.Thread(target=determine_key)
    key_thread.start()
