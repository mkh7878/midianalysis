import mido
import intervals
import time
from playsinewaves import play_sound

#Tells us if there are any midi devices attached, and if so, what they are called
#My midi keybaord is called "MPK mini 3"
def findMidiDevice():
    mido.set_backend('mido.backends.portmidi')
    input_names = mido.get_input_names()
    print("Available MIDI input devices:")
    for name in input_names:
        print(name)

if __name__ == '__main__':
    findMidiDevice()

def start_timer():
    return time.time()

def musicmusic():
    #start the timer
    #start_time = start_timer()

    # Set the backend to 'mido.backends.portmidi' or 'mido.backends.rtmidi'
    mido.set_backend('mido.backends.portmidi')

    # Get the name of the MIDI input device (your MIDI keyboard)
    input_name = mido.get_input_names()[0]  # Assuming your MIDI keyboard is the first device in the list

    # Open the MIDI input device
    with mido.open_input(input_name) as port:
        print(f"Connected to {input_name}...")

        # Create an empty list to store the captured notes
        captured_notes = []

        # Infinite loop to keep capturing MIDI messages
        while True:
            for message in port.iter_pending():

                #when a note is played on the midi keyboard
                if message.type == 'note_on':

                    #the current note value in relation to 0
                    current_note = message.note % 12

                    #add to the list of captured notes
                    captured_notes.append(current_note)

                    #print('current note value:', current_note)

                    #the key is the first note played, saved in the first spot in the list of captured notes
                    key = captured_notes[0]

                    #if the captured note value is higher than the key, it calculates the interval
                    #by subtracting key from note value
                    if current_note < key:
                        interval = 12 - (key - current_note)

                    elif current_note > key:
                        interval = current_note - key

                    else:
                        interval = 0

                    print(interval)

                    frequency = 2 ** ((message.note - 69) / 12) * 440
                    duration = 0.5  # Duration in seconds (you can adjust this)
                    play_sound(frequency, duration)

                    #prints the interval description from the "intervals" module
                    #print(intervals.intervals[interval])

                elif message.type == 'note_off':
                    print('----')

if __name__ == '__main__':
    musicmusic()