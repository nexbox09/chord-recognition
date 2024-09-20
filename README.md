# Audio Chord Analyzer

This application analyzes chords in audio files or YouTube videos, providing a web interface for uploading files or pasting YouTube URLs, and displays the detected chords over time.

## Prerequisites

The package is hosted on PyPI, but prior to installing that there are a few prerequisite steps. The following instructions assume the latest versions of Ubuntu, and it is recommended to use a modern 64-bit Linux system. That said, equivalent steps should work if you are using another OS.


- Python 3.9 (specifically this version)
- FFmpeg
- Libsndfile1
- Whisper
- Timidity
- 
 ``` sudo apt-get install libsndfile1  ``` - To read sound files.


 ``` sudo apt-get install timidity ``` To extract chord from MIDIs

  ``` sudo apt-get install ffmpeg ``` To extract from mp3 files and other formats



## Setup

1. Ensure you have Python 3.9 installed:
   ```
   python --version
   ```
   If not, download and install it from [python.org](https://www.python.org/downloads/release/python-390/)
   Or following this steps:

    Update the packages list and install the prerequisites:

```
sudo apt update
sudo apt install software-properties-common
```
Add the deadsnakes PPA to your system’s sources list:
```
sudo add-apt-repository ppa:deadsnakes/ppa
```

When prompted, press [Enter] to continue.

Once the repository is enabled, you can install Python 3.9 by executing:
```
sudo apt install python3.9
```

Verify that the installation was successful by typing:

```
python3.9 --version
```

```
Python 3.9.20
```
Install Python development headers:

```
sudo apt install python3.9-dev
```

That’s it. Python 3.9 is installed on your Ubuntu, and you can start using it.

2. Install pip3.9
You can install pip for python 3.9 the following way:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py
```
It is important you use python3.9 instead of just python3, to ensure pip is installed for python 3.9.

If you see any permissions errors, you may need to use
```
python3.9 get-pip.py --user
```
If you get an error like No module named 'distutils.util' when you run python3.9 get-pip.py, and you are on a Debian-based Linux distribution, run

```
sudo apt install python3.9-distutils
```
and then rerun your ```get-pip.py``` command. If you are not on a Debian-based distribution, use the equivalent command for your distribution's package manager.

3. Clone this repository:
   ```
   git clone https://github.com/nexbox09/chord-recognition.git
   cd chord-recognition
   ```

4. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

5. Install Whisper:
   ```
   pip install git+https://github.com/openai/whisper.git
   ```

## Project Structure

```
audio-chord-analyzer/
├── app.py
├── analysis/
│   ├── __init__.py
│   ├── audio_analyzer.py
│   ├── youtube_extractor.py
│   └── whisper_analyzer.py
├── web/
│   ├── __init__.py
│   ├── routes.py
│   └── templates/
│       └── upload.html
├── uploads/
│   └── .gitkeep
├── requirements.txt
└── README.md
```

## Running the Application

1. Ensure your virtual environment is activated.

2. From the project root directory, run:
   ```
   python app.py
   ```

3. Open a web browser and navigate to `http://localhost:5000`

4. Use the web interface to upload an audio file or paste a YouTube URL for analysis.

## Features

- Upload and analyze local audio files (WAV, MP3, OGG)
- Analyze audio from YouTube videos by URL
- Transcribe lyrics using OpenAI's Whisper
- Display chord changes over time using a chart
- List detected chords and transcribed lyrics with their timestamps

## Troubleshooting

- If you encounter disk space issues in VirtualBox:
  1. Shut down the virtual machine
  2. In the host system, use VBoxManage to resize the virtual disk:
     ```
     VBoxManage modifyhd "path/to/your/disk.vdi" --resize SIZE_IN_MB
     ```
  3. Start the VM and use `parted` and `resize2fs` to expand the partition and filesystem:
     ```
     sudo parted /dev/sda
     (parted) print
     (parted) resizepart 3 100%
     (parted) quit
     sudo resize2fs /dev/sda3
     ```

- Ensure FFmpeg is correctly installed and accessible in your system's PATH

- If you encounter issues with Whisper, ensure you have the latest version:
  ```
  pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
  ```

## Known Limitations

- The application requires significant computational resources, especially when using Whisper for transcription.
- Accuracy of chord detection and lyric transcription may vary depending on the quality of the input audio.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
