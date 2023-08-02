import numpy as np
import sounddevice as sd
import fluidsynth


def generate_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)
    return wave

def play_sound(frequency, duration, sample_rate=44100):
    audio_data = generate_sine_wave(frequency, duration, sample_rate)
    sd.play(audio_data, sample_rate, blocking=True)  # Use blocking=True to ensure audio is played