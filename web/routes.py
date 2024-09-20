# web/routes.py
from flask import render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
import traceback
import json
import urllib.parse
from analysis.chord_extractor import analyze_chords
from analysis.youtube_extractor import download_audio
from analysis.whisper_analyzer import transcribe_audio, get_lyrics_with_timestamps

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def configure_routes(app):
    @app.route('/', methods=['GET'])
    def index():
        return render_template('upload.html')

    @app.route('/analyze', methods=['POST'])
    def analyze():
        analysis_type = request.form.get('analysisType', 'chords_only')
        language = request.form.get('language', None) if analysis_type == 'chords_and_lyrics' else None
        model_size = request.form.get('modelSize', 'base') if analysis_type == 'chords_and_lyrics' else None

        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'})
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
        elif 'youtube_url' in request.form:
            youtube_url = request.form['youtube_url']
            try:
                filepath = download_audio(youtube_url, app.config['UPLOAD_FOLDER'])
            except Exception as e:
                return jsonify({'error': f'Error downloading YouTube audio: {str(e)}'}), 500
        else:
            return jsonify({'error': 'No file or YouTube URL provided'})

        try:
            # Extract chords
            chords = analyze_chords(filepath)
            
            result = {'chords': chords}
            
            if analysis_type == 'chords_and_lyrics':
                # Transcribe audio
                transcription = transcribe_audio(filepath, language, model_size)
                lyrics = get_lyrics_with_timestamps(transcription)
                
                result['lyrics'] = lyrics
                result['language'] = transcription['language']
            
            # Clean up uploaded file
            os.remove(filepath)
            
            # Encode results as URL parameter
            encoded_results = urllib.parse.quote(json.dumps(result))
            return redirect(url_for('show_results', results=encoded_results))
        except Exception as e:
            print(f"Error during processing: {str(e)}")
            print(traceback.format_exc())
            # If an error occurs during analysis, remove the file and return an error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500

    @app.route('/results')
    def show_results():
        return render_template('results.html')