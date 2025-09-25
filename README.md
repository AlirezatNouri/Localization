# Indoor Localization System (Audio-based GPS)

This project implements an **indoor localization system** that functions like an **audio-based GPS**. 

## Overview

Imagine being inside a large building (e.g., university, hospital, mall) and searching for a specific room or object.  
GPS signals are weak or unavailable indoors, so this system provides **an alternative positioning method**:

- **Embedded speakers** emit **ultrasonic signals** (inaudible to humans).  
- **Microphones** detect these ultrasonic sounds.  
- The system **processes the signals** and determines the **location of the sound source**.  
- Users access the system via a **locally hosted web interface**, where they can:  
  - Search for a room or object.  
  - Be guided toward the corresponding speaker location.  

Even **small objects** can be tracked if they are tagged with a mini speaker.  

---
## Table of Contents

1. [Features](#features)
2. [Tech Stack](#Tech-Stack) 
3. [Repository Structure](#Repository-Structure)   
4. [Installation & Usage](#Installation-&-Usage)
5. [Future Improvements](#Future-Improvements)

---   
## Features

- Indoor navigation without GPS  
- Detects and locates ultrasonic signals  
- Guides users toward the desired location  
- Web-based interface (accessible via browser)  
- Object tracking with speaker tags  

---

## Tech Stack

- **Python** (signal processing, backend logic)  
- **HTML** (frontend interface)  
- **Flask / local server** for browser-based interaction  
- **Audio hardware**:  
  - Ultrasonic speakers (emitters)  
  - Microphones (receivers)  

---

## Repository Structure
Localization/
│── app.py # Web application / server
│── main.py # Core localization logic
│── index.html # Web interface


---

## Installation & Usage

1.Install dependencies:

pip install -r requirements.txt


2.Run the app:

python app.py


3.Open your browser:

http://127.0.0.1:5000

---
## Future Improvements

Improve accuracy with advanced signal processing

Multi-microphone triangulation for precise positioning

Mobile-friendly UI

Scalable for large buildings (multi-floor support)

Integration with IoT devices and smart building systems

