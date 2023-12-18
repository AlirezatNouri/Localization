from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from scipy.signal import correlate, butter, filtfilt
import sounddevice as sd
import time

app = Flask(__name__)
CORS(app)

def generate_chirp_signal(fs, duration, f0, f1):
    t = np.linspace(0, duration, int(fs*duration))
    chirp_signal = np.sin(2*np.pi*(f0*t + (f1-f0)*t**2/(2*duration)))
    return chirp_signal

def tdoa(recording1, recording2, fs):
    correlation = correlate(recording1, recording2, 'full')
    delay_samples = correlation.argmax() - (len(recording1) - 1)
    time_delay = delay_samples / fs
    return abs(time_delay), correlation

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    filtered_data = filtfilt(b, a, data)
    return filtered_data

@app.route('/compute_distances', methods=['POST'])
def compute_distances():
    time.sleep(5)  # Adding a delay

    fs = 48000
    duration = 5
    f0 = 21000
    f1 = 24000

    chirp_signal = generate_chirp_signal(fs, duration, f0, f1)

    recording1 = sd.playrec(chirp_signal, samplerate=fs, channels=2, blocking=True)
    recording1_left = recording1[:, 0]

    time.sleep(10)  # 10 seconds delay between recordings

    recording2 = sd.playrec(chirp_signal, samplerate=fs, channels=2, blocking=True)
    recording2_left = recording2[:, 0]

    lowcut = 20800
    highcut = 23200
    filtered_recording1 = bandpass_filter(recording1_left, lowcut, highcut, fs)
    filtered_recording2 = bandpass_filter(recording2_left, lowcut, highcut, fs)

    time_delay, _ = tdoa(filtered_recording1, filtered_recording2, fs)
    speed_of_sound = 343  # Speed of sound in air in m/s
    distance_difference = time_delay * speed_of_sound

    d_mics = 1.6
    distance_source_to_mic1 = (d_mics + distance_difference) / 2
    distance_source_to_mic2 = (d_mics - distance_difference) / 2

    result = {
        'distance_to_microphone_1': distance_source_to_mic1 * 100,
        'distance_to_microphone_2': distance_source_to_mic2 * 100,
        'distance_difference_between_microphones': distance_difference * 100
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
