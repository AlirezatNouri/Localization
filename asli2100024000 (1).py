import numpy as np
from scipy.signal import correlate, butter, filtfilt
import sounddevice as sd
import matplotlib.pyplot as plt
import time

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
    b, a = butter(order, [lowcut, highcut], btype='band', fs=fs)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

if __name__ == '__main__':
    fs = 48000  # تنظیم مجدد فرکانس نمونه‌برداری
    duration = 5
    f0 = 21000
    f1 = 24000

    chirp_signal = generate_chirp_signal(fs, duration, f0, f1)

    # Play and record the first instance as microphone 1
    recording1 = sd.playrec(chirp_signal, samplerate=fs, channels=2, blocking=True)
    recording1_left = recording1[:, 0]
    recording1_right = recording1[:, 1]

    # A delay of 10 seconds
    time.sleep(10)

    # Play and record the second instance as microphone 2
    recording2 = sd.playrec(chirp_signal, samplerate=fs, channels=2, blocking=True)
    recording2_left = recording2[:, 0]
    recording2_right = recording2[:, 1]
    
    lowcut = 20800
    highcut = 23200
    filtered_recording1 = bandpass_filter(recording1_left, lowcut, highcut, fs)
    filtered_recording2 = bandpass_filter(recording2_left, lowcut, highcut, fs)

    time_delay, correlation = tdoa(filtered_recording1, filtered_recording2, fs)
    speed_of_sound = 343  # Speed of sound in air in m/s
    distance_difference = time_delay * speed_of_sound

    d_mics = 1.2
    distance_source_to_mic1 = (d_mics + distance_difference) / 2
    distance_source_to_mic2 = (d_mics - distance_difference) / 2

    print("Distance to Microphone 1:", distance_source_to_mic1 * 100, "cm")
    print("Distance to Microphone 2:", distance_source_to_mic2 * 100, "cm")
    print("Distance difference between microphones:", distance_difference * 100, "cm")

    # Plotting
    plt.figure(figsize=(15, 10))

    plt.subplot(3, 1, 1)
    plt.plot(filtered_recording1)
    plt.title("Recording 1 Left (Filtered)")
    
    plt.subplot(3, 1, 2)
    plt.plot(filtered_recording2)
    plt.title("Recording 2 Left (Filtered)")

    plt.subplot(3, 1, 3)
    plt.plot(correlation)
    plt.title("Cross-Correlation between Recording 1 and Recording 2")
    
    plt.tight_layout()
    plt.show()
