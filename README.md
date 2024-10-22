# WAVE-steganography

## Help page
The output of `python3 main.py --help` command, displaying a list of all available commands in the application:
```
usage: main.py [-h] [-hl fileName secretMessage] [-el fileName] [-hp fileName secretMessage] [-ep fileName] [-s path]

Steganography app manager

options:
  -h, --help            show this help message and exit
  -hl fileName secretMessage, --hide-lsb fileName secretMessage
                        hide secret message using LSB method in specified file
  -el fileName, --extract-lsb fileName
                        extract data using LSB method from specified file
  -hp fileName secretMessage, --hide-phase-coding fileName secretMessage
                        hide data using Phase Coding method in specified file
  -ep fileName, --extract-phase-coding fileName
                        extract data using Phase Coding method from specified file
  -s path, --show path  show all wav files in specified directory path. Type '.' for current directory.
```
