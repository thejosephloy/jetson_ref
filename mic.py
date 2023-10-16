import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import threading

# Global Variables
audio_data_global = np.array([])

def update_plot():
    global audio_data_global
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1)
    line1, = ax1.plot([], [])
    line2, = ax2.plot([], [])
    
    while True:
        if len(audio_data_global) > 0:
            # Perform FFT and get frequencies
            fft_data = np.fft.fft(audio_data_global)
            freqs = np.fft.fftfreq(len(fft_data), 1/44100)

            # Update the plots
            line1.set_data(np.arange(len(audio_data_global)), audio_data_global)
            line2.set_data(freqs, np.abs(fft_data))
            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()
            fig.canvas.flush_events()

def callback(in_data, frame_count, time_info, flag):
    global audio_data_global
    audio_data_global = np.frombuffer(in_data, dtype=np.int16)
    return (in_data, pyaudio.paContinue)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
DEVICE_INDEX = 11

# Start Plotting Thread
plot_thread = threading.Thread(target=update_plot)
plot_thread.daemon = True
plot_thread.start()

# Open Stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=DEVICE_INDEX,
                stream_callback=callback)

# Start the stream
stream.start_stream()

# Keep the stream alive
try:
    while stream.is_active():
        pass
except KeyboardInterrupt:
    # Stop stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.ioff()

