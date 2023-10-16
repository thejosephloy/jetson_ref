import pyaudio
import numpy as np

def callback(in_data, frame_count, time_info, flag):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    print("Audio Data:", audio_data)
    return (in_data, pyaudio.paContinue)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096  # Increased buffer size
DEVICE_INDEX = 11

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

