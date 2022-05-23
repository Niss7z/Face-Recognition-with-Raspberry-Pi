# Face-Recognition-Security-System-With-Raspberry-Pi
This is a Python 3 computer vision project which utilises face recognition A.I, a Raspberry pi 4, a usb webcam and a servo to open a door lock. 

## Prerequisites
Python 3, OpenCV, and  Raspberry Pi (model 3 or above) are needed. Python packages such as numpy, CMake and face-recognition also need to be installed.

OpenCV can be installed using ``pip``
``` 
pip install opencv-python
pip install opencv-contrib-python
```
CMake and face-recognition can also be installed using ``pip``
```
pip install cmake
pip install face-recognition
```
Numpy can be installed using ``sudo apt-get``
```
sudo apt-get install python3-numpy
```

## Installation
First specify your directory using terminal: 
``` git
cd your/path/name
```
Then, copy or type the following:
``` git
git clone https://github.com/Niss7z/Face-Recognition-with-Raspberry-Pi.git
```

## Project Structure
```
├── faceTrain
│   ├── training-image.png
├── venv
│   ├── bin
│   ├── lib
│   │   ├── .gitignore
│   │   ├── pyvenv.cfg 
├── FaceRecogniton.py
```
This is essentially the project structure.

All training images go inside the ``faceTrain`` folder.  Virtual environments and the likes go inside the ``venv``
folder. Main code is written inside FaceRecognition.py file.

## Licence
Creative Commons Zero v1.0 Universal
