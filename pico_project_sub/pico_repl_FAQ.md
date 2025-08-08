# Raspberry Pi Pico – MicroPython REPL FAQ

## What is REPL?
REPL stands for **Read–Eval–Print–Loop**. It is an interactive prompt where you can type Python commands and get immediate results.

## Accessing REPL on macOS (Zsh)
**Using mpremote:**
```zsh
mpremote connect /dev/tty.usbmodemXXXX
```
**Using screen:**
```zsh
screen /dev/tty.usbmodemXXXX 115200
```
**Exit screen:**
```
Ctrl-A, then Ctrl-\, then y
```

## Basic Commands
```python
>>> 2 + 3        # Math
>>> print('Hi')  # Print text
>>> help()       # Help menu
>>> help('modules') # List modules
```

## Filesystem Commands
```python
import os
os.listdir()                  # List files
os.remove('file.py')           # Delete file
os.rename('old.py', 'new.py')  # Rename file
```

## File Info & Storage
```python
import os
for f in os.listdir():
    print(f, os.stat(f)[6], 'bytes')

stats = os.statvfs('/')
total = stats[0] * stats[2]
free = stats[0] * stats[3]
print('Total:', total, 'Free:', free)
```

## Running Code from REPL
```python
exec(open('file.py').read())   # Run a script
import mymodule                 # Import and run module code
from mymodule import myfunc; myfunc()  # Run function
```

## Stopping Code
```
Ctrl-C     # Stop running program in REPL
Ctrl-D     # Soft reboot the Pico
```

## Tips
- `boot.py` runs on startup (setup code)
- `main.py` runs after `boot.py` (main program)
- Use safe mode to bypass `main.py` if it locks up (hold BOOTSEL on reset for certain firmware modes)
