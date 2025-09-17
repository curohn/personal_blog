# DJI Tello Drone Controller

> **Note**: This project was developed with significant help from LLM agents (Claude and ChatGPT) for code generation, documentation, and problem-solving. It's been a great way to learn drone programming while leveraging AI assistance.

## What This Is

I built this Python controller for my DJI Tello drone because the basic controls weren't cutting it. I wanted to do more complex flight patterns, capture photos automatically, and have better safety features than what comes out of the box.

The project started as a way to learn about drone programming, but it's turned into a pretty solid SDK that can handle everything from basic takeoff/landing to complex geometric flight patterns.

## What It Does

- **Flight Control**: All the basic movements plus some fancy stuff like automated patterns
- **Camera**: Live video streaming and photo capture 
- **Safety Features**: Battery monitoring, emergency stops, connection checks
- **Complex Patterns**: Pre-programmed flights like squares, circles, and flip sequences
- **Computer Vision Ready**: Set up to work with OpenCV for autonomous navigation (still working on this part)

## Project Structure

The code is organized pretty simply:

```
tello_controller/
├── src/
│   ├── tello_controller.py    # Main drone interface
│   ├── flight_control.py      # The fun flight patterns
│   └── utils.py              # Helper stuff
├── examples/
│   ├── basic_flight_demo.py   # Simple demo to test everything works
│   └── advanced_patterns.py   # The cool stuff
├── photos/                    # Where captured photos go
└── tests/                     # Unit tests (because crashes are expensive)
```

## Getting Started

### What You Need
- A DJI Tello or Tello EDU drone (obviously)
- Python 3.8+ on your computer
- WiFi connection
- Somewhere safe to fly (not your living room - learned that the hard way)

### Setup

Clone the repo and install dependencies:
```bash
git clone https://github.com/curohn/tello_controller.git
cd tello_controller
pip install -r requirements.txt
```

Connect to your Tello:
1. Turn on the drone
2. Connect your computer to the Tello's WiFi network (something like TELLO-XXXXXX)
3. Wait for the connection light to go solid
4. Run one of the flight files:

### Basic Usage

```bash
python src/flight_control.py
```

## Available Commands

type `help` for a list of available commands

## Safety Stuff (Important!)

**Please don't crash your drone.** I learned some of these the hard way:

- Fly outside or in a big space - drones are bigger than you think when they're spinning
- Check battery constantly - land when it gets to 20% or the drone will land itself wherever it is
- Keep a strong WiFi connection - if you lose connection, the drone will hover and land on its own
- Don't fly in wind, rain, or when you can't see well
- Know your local drone rules

## What I Learned

This project was a great way to dive into drone programming and learn about:
- Real-time communication with hardware over WiFi
- Next up: Computer vision basics (still working on the advanced stuff)
- Working with AI assistants for code generation and problem-solving

## Future Plans

- Better autonomous navigation with OpenCV
- More complex flight patterns
- Maybe some basic AI for obstacle avoidance

## Resources I Used

- [DJI Tello SDK Documentation](https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf) - The official docs
- [djitellopy](https://github.com/damiafuentes/DJITelloPy) - Python library that does the heavy lifting
- [OpenCV Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) - For computer vision stuff
- Various drone forums and Reddit threads when things broke

The AI assistants (Claude and ChatGPT) were incredibly helpful for generating boilerplate code, suggesting safety features I hadn't thought of, and debugging connection issues.

---

This has been one of my more fun projects - there's something really satisfying about writing code that makes a physical object fly around. If you build something similar, I'd love to see it!