import pyaudio
import wave
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# Audio recording settings
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono audio
RATE = 44100  # 44.1kHz sampling rate
FILENAME = "recording.wav"  # Temporary audio file

def record_audio():
    """Records audio until the user stops."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)
    print("Recording... Press Ctrl+C to stop.")
    
    frames = []
    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        print("Recording stopped.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recording to a file
    with wave.open(FILENAME, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
    
    print(f"Audio saved to {FILENAME}")

def transcribe_audio(file_path):
    """Transcribes audio using OpenAI."""
    print("Sending audio for transcription...")
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
model="whisper-1", 
file=audio_file
)
    print(transcription.text)
    print("Transcription completed!")
    return transcription.text

def main():
    record_audio()
    transcription = transcribe_audio(FILENAME)
    print("\nTranscription:\n", transcription)

if __name__ == "__main__":
    main()
