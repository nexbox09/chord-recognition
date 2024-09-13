# analysis/chord_extractor.py
from chord_extractor.extractors import Chordino
from chord_extractor import clear_conversion_cache

def analyze_chords(filepath):
    try:
        chordino = Chordino()
        clear_conversion_cache()
        results = chordino.extract_many([filepath])
        
        chords = []
        for labelled_chord_sequence in results:
            for chord_change in labelled_chord_sequence.sequence:
                chords.append({
                    'chord': chord_change.chord,
                    'timestamp': chord_change.timestamp
                })
        
        return chords
    except Exception as e:
        print(f"Error in analyze_chords: {str(e)}")
        return []