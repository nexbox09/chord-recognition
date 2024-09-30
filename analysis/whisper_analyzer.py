import whisper_timestamped as whisper
import librosa

def transcribe_audio(filepath, model_size='base'):
    """
    Transcribe el audio usando el modelo Whisper con marcas de tiempo a nivel de palabra.
    """
    # Cargar el modelo
    model = whisper.load_model(model_size)
    # Cargar el audio
    audio = whisper.load_audio(filepath)
    # Transcribir el audio
    result = whisper.transcribe(model, audio)
    return result

def divide_audio_into_segments(audio_file, segment_duration=2.0):
    """
    Divide el audio en segmentos fijos de duración dada en segundos.
    """
    y, sr = librosa.load(audio_file, sr=None)
    total_duration = librosa.get_duration(y=y, sr=sr)
    segments = [i * segment_duration for i in range(int(total_duration // segment_duration) + 1)]
    return segments

def get_lyrics_with_fixed_segments(transcription, segment_timestamps):
    """
    Asigna cada palabra a uno de los segmentos fijos de tiempo.
    """
    lyrics_with_segments = []
    num_segments = len(segment_timestamps) - 1
    segment_duration = segment_timestamps[1] - segment_timestamps[0]

    # Inicializar la lista de segmentos
    for i in range(num_segments):
        lyrics_with_segments.append({
            'start': segment_timestamps[i],
            'end': segment_timestamps[i+1],
            'text': ''
        })

    # Asignar palabras a los segmentos correspondientes
    for segment in transcription['segments']:
        for word_info in segment.get('words', []):
            word_start = word_info['start']
            word_text = word_info['text']

            # Encontrar el índice del segmento al que pertenece la palabra
            segment_index = int((word_start - segment_timestamps[0]) // segment_duration)
            segment_index = max(0, min(segment_index, num_segments - 1))

            # Agregar la palabra al texto del segmento
            if lyrics_with_segments[segment_index]['text']:
                lyrics_with_segments[segment_index]['text'] += ' ' + word_text
            else:
                lyrics_with_segments[segment_index]['text'] = word_text

    return lyrics_with_segments

def transcribe_and_segment(filepath, model_size='base', segment_duration=2.0):
    """
    Transcribe el audio y ajusta los timestamps dividiendo el audio en segmentos fijos.
    """
    # Transcribir usando Whisper con marcas de tiempo precisas
    transcription = transcribe_audio(filepath, model_size=model_size)

    # Dividir el audio en segmentos fijos
    segment_timestamps = divide_audio_into_segments(filepath, segment_duration=segment_duration)

    # Asignar las palabras a los segmentos
    lyrics = get_lyrics_with_fixed_segments(transcription, segment_timestamps)

    return lyrics