import OPi.GPIO as GPIO  # Asegúrate de usar la librería correcta para Orange Pi
import time

# Mapeo de acordes a pines GPIO
notes_gpio_mapping = {
    'C': 11,  # Cambiar estos números según el mapeo de los pines en tu Orange Pi
    'C#': 12,
    'D': 13,
    'D#': 15,
    'E': 16,
    'F': 18,
    'F#': 22,
    'G': 7,
    'G#': 3,
    'A': 5,
    'A#': 24,
    'B': 26
}

def setup_gpio():
    """
    Inicializa los pines GPIO y los configura como salida.
    """
    GPIO.setmode(GPIO.BOARD)
    for pin in notes_gpio_mapping.values():
        GPIO.setup(pin, GPIO.OUT)

def play_chord(chord):
    """
    Toca un acorde activando los pines GPIO correspondientes.
    
    :param chord: Una lista de notas (ej. ['C', 'E', 'G'] para un acorde de C mayor)
    """
    # Apagar todas las notas antes de activar el acorde actual
    for pin in notes_gpio_mapping.values():
        GPIO.output(pin, GPIO.LOW)

    # Activar los pines GPIO para las notas del acorde
    for note in chord:
        if note in notes_gpio_mapping:
            GPIO.output(notes_gpio_mapping[note], GPIO.HIGH)
            time.sleep(0.5)  # Mantener la nota por 0.5 segundos

    # Apagar las notas después de tocarlas
    for pin in notes_gpio_mapping.values():
        GPIO.output(pin, GPIO.LOW)

def cleanup_gpio():
    """
    Limpia la configuración de los pines GPIO al finalizar.
    """
    GPIO.cleanup()
