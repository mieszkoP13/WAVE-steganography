# WAVE-steganography

## Help Page
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

## Application Class Structure
A diagram of all the main classes of the application, ensuring the operation of the application in user mode.

<img src="https://github.com/user-attachments/assets/4fc0ceb7-d89f-444a-966f-46f0c7e23a48" alt="classes" width="800" />


An additional class used for testing the application, not intended for the regular user.

<img src="https://github.com/user-attachments/assets/2323ba8d-ee25-4c23-8f8d-f0b24035851a" alt="classes" width="800" />

An additional class used for generating signal charts, not intended for the regular user.

<img src="https://github.com/user-attachments/assets/b36e0e45-369d-4eee-bb7d-18b0adbbd9b5" alt="classes" width="800" />
