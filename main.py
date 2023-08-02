import mido
import intervals
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
import circle
from circle import CircleApp, CircleWidget
import threading
from common import circle_width



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

import mido

def print_notes():
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
                if message.type == 'note_on':
                    captured_notes.append(message.note)
                    current_note = message.note
                    interval = abs(captured_notes[0] - current_note)
                    interval = interval % 12
                    print(intervals.intervals [interval])
                    circle_width = interval * 100

                #elif message.type == 'note_off':
                    # print(captured_notes)
                    # music_key = captured_notes[0]
                    # print('music key =',captured_notes[0])

if __name__ == '__main__':

    midi_thread = threading.Thread(target=print_notes, daemon=True)
    midi_thread.start()

    circle_app = CircleApp()  # Create an instance of CircleApp
    circle_app.run()



