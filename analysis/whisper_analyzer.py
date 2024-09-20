# analysis/whisper_analyzer.py
import whisper
import os

def transcribe_audio(audio_path, language=None, model_size="base"):
    model = whisper.load_model(model_size)
    
    # Use basic options available in older versions
    options = whisper.DecodingOptions(
        language=language,
        without_timestamps=False,
        fp16=False  # Use fp32 for potentially higher accuracy
    )
    
    # Transcribe with custom options
    result = model.transcribe(audio_path, **options.__dict__)
    
    return result

def get_lyrics_with_timestamps(transcription):
    lyrics = []
    
    for segment in transcription['segments']:
        start = segment['start']
        end = segment['end']
        text = segment['text'].strip()
        
        # Split long segments into smaller parts
        words = text.split()
        if len(words) > 10:  # If segment has more than 10 words, split it
            mid = len(words) // 2
            duration = end - start
            mid_time = start + (duration / 2)
            
            lyrics.append({
                'text': ' '.join(words[:mid]),
                'start': start,
                'end': mid_time
            })
            lyrics.append({
                'text': ' '.join(words[mid:]),
                'start': mid_time,
                'end': end
            })
        else:
            lyrics.append({
                'text': text,
                'start': start,
                'end': end
            })
    
    return lyrics