This repository contains the software for the Chichera calculator device (the calculator itself is named "Chichera"; this project provides its software), developed for a Raspberry Pi Zero 2 W–based handheld calculator.

## Description
Control and user-interface software for the Chichera calculator: input handling (GPIO buttons / USB keyboard), display management, and support for basic and extendable advanced operations.

## Features
- UI optimized for small integrated displays
- Input via GPIO buttons or USB keyboard
- Basic arithmetic and extensible function support
- Hardware configuration via configuration files

## Requirements
- Raspberry Pi Zero 2 W running Raspberry Pi OS
- Python 3.8+ and pip
- GPIO and GUI libraries (e.g., gpiozero, RPi.GPIO, pygame or tkinter)
- Configuration files for pin mapping and display

## Installation
1. Clone the repository: git clone <repo-url>
2. Change to the project directory: cd chichera_calcolatrice
3. Create and activate a virtual environment:
    - python3 -m venv venv
    - source venv/bin/activate
4. Install dependencies: pip install -r requirements.txt
5. Configure pin and display settings according to the documentation
6. Run: python main.py

## Usage
Run the software on the Raspberry Pi with the display and buttons connected. Follow on-screen instructions to perform calculations and edit hardware settings via the configuration files.

## Contributing
Issues and pull requests are welcome. Please follow the project contribution guidelines and CODE_OF_CONDUCT if present.

## License
See the LICENSE file for license details (e.g., MIT).
