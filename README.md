# CS2 Bot Aim Sandbox

Standalone CS2-style bot/aim-training simulator.

## Controls
- Left click: shoot
- E: toggle ESP
- A: toggle simulated aim assist
- R: reset
- Esc: quit

## Build locally
python -m pip install pyinstaller
pyinstaller --onefile --windowed --name CS2_Bot_Sandbox main.py

The EXE will be in dist/.

## Safety boundary
This is standalone. It does not attach to CS2, read game memory, inject code, manipulate the CS2 process, or interact with VAC.
