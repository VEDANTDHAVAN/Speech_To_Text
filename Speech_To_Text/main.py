import whisper

model = whisper.load_model('base')

import gradio as gr # Import gradio as gr
import time

def transcribe(audio):
  #time.sleep(3)
  #step 1: load audio
  audio = whisper.load_audio(audio)
  audio = whisper.pad_or_trim(audio)

  #step 2: make a log-Mel Spectrogram and move to the same device as the model
  mel = whisper.log_mel_spectrogram(audio).to(model.device)

  #step 3: detect the spoken laguage
  _, probs = model.detect_language(mel)
  print(f"Detected language: {max(probs, key=probs.get)}")

  #step 4: decode the audio
  options = whisper.DecodingOptions()
  result = whisper.decode(model, mel, options)

  #step 5: print the recognized text
  return result.text

gr.Interface( # Use gr.Interface
    title = 'Speech to Text using API',
    fn=transcribe,
    inputs=[
        # Removed the 'source' argument and changed 'type' to 'microphone'.
        gr.Audio(type="filepath")
    ],
    outputs=[
        "textbox"
    ],
    live=True).launch()