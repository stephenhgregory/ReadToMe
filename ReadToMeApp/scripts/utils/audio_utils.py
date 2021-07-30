''' Contains functions for recording, playing back, and manipulating audio '''

import pyaudio
import wave


def record_audio(filename: str, chunk_size: int = 1024, format: int = pyaudio.paInt16, num_channels: int = 1, sample_rate: int = 44100, 
                 num_seconds: int = 5, hear_voice_playback: bool = False):
    '''
    TODO: Create docs for this function
    '''
    # Initiialize PyAudio object
    p = pyaudio.PyAudio()
    # Initialize list of frames
    frames = []
    # Open stream object as input & output
    stream = p.open(format=format,
                    channels=num_channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk_size)
    # Record the audio
    for i in range(int(sample_rate / chunk_size * num_seconds)):
        audio_data = stream.read(chunk_size)
        if hear_voice_playback:
            stream.write(audio_data)
        frames.append(audio_data)
    # Stop recording and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate pyaudio object
    p.terminate()
    # Return the frames
    return frames


def save_audio_file(py_audio, frames, filename: str, sample_rate: int = 44100, format: int = pyaudio.paInt16, num_channels: int = 1):
    '''
    TODO: Better Docs
    '''
    # Open the .wav file in "write bytes" mode
    wf = wave.open(filename, "wb")
    # Set the number of channels
    wf.setnchannels(num_channels)
    # Set the sample format
    wf.setsampwidth(py_audio.get_sample_size(format))
    # Set the sample rate
    wf.setframerate(sample_rate)
    # Write the frames as bytes
    wf.writeframes(b"".join(frames))
    # close the file
    wf.close()


def record_and_save_audio(filename: str, chunk_size: int = 1024, format: int = pyaudio.paInt16, num_channels: int = 1, sample_rate: int = 44100, 
                 num_seconds: int = 5, hear_voice_playback: bool = False):
    '''
    TODO: Create docs for this function
    '''
    # Record the audio file
    frames = record_audio(filename=filename, chunk_size=chunk_size, format=format, num_channels=num_channels, sample_rate=sample_rate, num_seconds=num_seconds, hear_voice_playback=hear_voice_playback)
    # Save the audio file
    save_audio_file(frames=frames, filename=filename, format=format, num_channels=num_channels)
