# analysis/whisper_analyzer.py
import whisper
import os

def transcribe_audio(audio_path, language=None, model_size="base"):
    model = whisper.load_model(model_size)
    
    if language:
        result = model.transcribe(audio_path, language=language)
    else:
        result = model.transcribe(audio_path)
    
    return result

def get_lyrics_with_timestamps(transcription):
    lyrics = []
    for segment in transcription['segments']:
        lyrics.append({
            'text': segment['text'],
            'start': segment['start'],
            'end': segment['end']
        })
    return lyrics