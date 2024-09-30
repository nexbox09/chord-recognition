from flask import render_template, request, jsonify, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename
from analysis.chord_extractor import analyze_chords
from analysis.whisper_analyzer import transcribe_and_segment
from analysis.youtube_extractor import download_audio

# Extensiones de archivos permitidas
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

def allowed_file(filename):
    """
    Verifica si un archivo tiene una extensión permitida.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def configure_routes(app):
    """
    Configura las rutas de la aplicación Flask.
    """
    @app.route('/', methods=['GET'])
    def index():
        """
        Ruta principal que muestra la página de carga de archivos.
        """
        return render_template('upload.html')

    @app.route('/analyze', methods=['POST'])
    def analyze():
        """
        Ruta para analizar un archivo subido o un video de YouTube.
        """
        analysis_type = request.form.get('analysisType', 'chords_only')
        model_size = request.form.get('modelSize', 'base') if analysis_type == 'chords_and_lyrics' else None

        # Manejo de archivos subidos
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No se seleccionó un archivo'}), 400
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
        elif 'youtube_url' in request.form:
            # Manejo de URL de YouTube
            youtube_url = request.form['youtube_url']
            try:
                filepath = download_audio(youtube_url, app.config['UPLOAD_FOLDER'])
            except Exception as e:
                return jsonify({'error': f'Error al descargar el audio de YouTube: {str(e)}'}), 500
        else:
            return jsonify({'error': 'No se proporcionó archivo o URL de YouTube'}), 400

        try:
            # Análisis según el tipo seleccionado
            if analysis_type == 'chords_only':
                # Solo analizar acordes
                chords = analyze_chords(filepath)
                if not chords:
                    return jsonify({"error": "No se detectaron acordes"}), 400
                result = {'chords': chords}
            else:
                # Analizar tanto acordes como letras con Whisper
                chords = analyze_chords(filepath)
                lyrics = transcribe_and_segment(filepath, model_size=model_size)
                result = {'chords': chords, 'lyrics': lyrics}

            # No eliminamos el archivo, ya que se necesita para la reproducción en la página de resultados
            # Obtener la URL relativa del archivo de audio para usarla en la plantilla
            audio_url = os.path.join('/uploads', os.path.basename(filepath))

            # Convertir los resultados en JSON
            results_json = json.dumps(result)

            # Renderizar la plantilla 'results.html' pasando el archivo de audio y los resultados
            return render_template('results.html', audio_url=audio_url, results_json=results_json)

        except Exception as e:
            print(f"Error durante el procesamiento: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/results')
    def show_results():
        """
        Ruta para mostrar los resultados de análisis (acordes y letras).
        """
        return render_template('results.html')
