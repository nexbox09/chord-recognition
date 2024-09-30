import wiringpi
import time

# Mapeo de acordes a pines GPIO
notes_gpio_mapping = {
    'C': 3,  # PH5
    'C#': 5,  # PH4
    'D': 7,  # PC9
    'D#': 11, # PC6
    'E': 13, # PC5
    'F': 15, # PC8
    'F#': 19, # PH7
    'G': 21, # PH8
    'G#': 23, # PH6
    'A': 22, # PC7
    'A#': 24, # PH9
    'B': 26  # PC10
}

# Configurar los pines GPIO como salida
def setup_gpio():
    """
    Inicializa los pines GPIO y los configura como salida.
    """
    wiringpi.wiringPiSetup()
    for pin in notes_gpio_mapping.values():
        wiringpi.pinMode(pin, 1)  # 1 = salida

# Activar las notas en los pines GPIO correspondientes a un acorde
def play_chord(chord):
    """
    Toca un acorde activando los pines GPIO correspondientes.
    
    :param chord: Una lista de notas (ej. ['C', 'E', 'G'] para un acorde de C mayor)
    """
    # Apagar todas las notas antes de activar el acorde actual
    for pin in notes_gpio_mapping.values():
        wiringpi.digitalWrite(pin, 0)

    # Activar los pines GPIO para las notas del acorde
    for note in chord:
        if note in notes_gpio_mapping:
            wiringpi.digitalWrite(notes_gpio_mapping[note], 1)
            time.sleep(0.5)  # Mantener la nota por 0.5 segundos
        else:
            print(f"Nota {note} no encontrada en el mapeo de GPIO")

# Apagar todas las notas (resetear los GPIO)
def stop_all_notes():
    """
    Apaga todas las notas desactivando los pines GPIO.
    """
    for pin in notes_gpio_mapping.values():
        wiringpi.digitalWrite(pin, 0)
