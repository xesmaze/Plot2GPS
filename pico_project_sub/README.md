Project for storing the mini-scripts written for Raspberry Pi Pico
on MacOSX

The connections:
```
U1-Raspberry Pi- Pico
 |--U2 -LoRa Module : Waveshare Pico-LoRa-SX126X
 |--U3 -I2C-Mini-OLED Display 
 |--U4 -Solar Power Manager 5V : DFROBOT
   |-Battery
   |-AK50x50 Solar Cell
```
To program the pico
## Raspberry Pi Pico (or Pico W) — From Zero to “Hello, World” on macOS (Zsh)

## 0) What You’ll Need
- Raspberry Pi **Pico** (or **Pico W** for Wi-Fi)
- **USB data** cable (not charge-only)
- macOS with **Zsh** (default on modern macOS)

---

## 1) Flash MicroPython (one-time)
1. **Unplug** the Pico.
2. **Hold** the **BOOTSEL** button.
3. **Plug in** the USB while holding BOOTSEL → drive **RPI-RP2** appears in Finder window.
4. Download **MicroPython UF2** for your board from the official site.

   → Current version included here is 20250415-v1.25.0
5. **Drag-drop** the `.uf2` onto **RPI-RP2**.  
   → The drive ejects automatically and Pico reboots into MicroPython.

---

## 2) Install `mpremote` (via pipx if running homebrew as a package manager)
```zsh
brew install pipx
pipx ensurepath
pipx install mpremote
```
`mpremote` lets you interact with Pico, upload files, and run scripts.

## 3) Find the Pico's serial port
Open a MacOSx Terminal window and run
```zsh
ls /dev/tty.usbmodem*
```
Example Result :
```
/dev/tty.usbmodem1401
```
## 4) Open a MicroPython REPL
### Option A: w/ `mpremote` (recommended)

```zsh
mpremote connect /dev/tty.usbmodem1401
```
This will start a python commandline prompt on Pico for direct interfacing
In REPL try :
```python
print("Hello, Pico!")
```
Exit REPL: Ctrl-] (stop running script: Ctrl-C)

### Option B: Use `screen`
#### There is a native terminal based access program for interfacing with Pico
called `screen` that can be run natively on OSX terminal

```zsh
screen /dev/tty.usbmodem1401 115200
```
Exit with: `Ctrl-A → Ctrl-\ → y`

## 5) First Script (Blink the LED)
create `main.py` on OSX:

```python
from machine import Pin
import time

led = Pin("LED", Pin.OUT)
while True:
    led.toggle()
    time.sleep(0.5)
```    
Upload to Pico and run:

```zsh
mpremote connect /dev/tty.usbmodem1401 fs cp main.py :
mpremote connect /dev/tty.usbmodem1401 reset
```

## 6) Project Workflow
The code can be edited on the local OSX folder- and can be accessed through regular
system python interpreter. 
If compiled into `my_module.py`

The module can then be uploaded to Pico:

```zsh
mpremote connect /dev/tty.usbmodem1401 fs cp my_module.py :
mpremote connect /dev/tty.usbmodem1401 run my_module.py
```
The upload to Pico from local Pico module can be automated with a shell script
such as `deploy.sh` in the project folder on OSX:

```zsh
#!/bin/zsh
PORT=/dev/tty.usbmodem1401
mpremote connect $PORT fs cp main.py :
mpremote connect $PORT reset
```
To Make the shell script executable, do:

```zsh
chmod +x deploy.sh
```
## 7) If Using Pico W: Connect to Wi-Fi
`wifi.py`
import network, time
```python
def wifi_connect(ssid, password, timeout=15):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        t0 = time.time()
        while not wlan.isconnected():
            if time.time() - t0 > timeout:
                raise RuntimeError("Wi-Fi connect timeout")
            time.sleep(0.2)
    return wlan.ifconfig()
```
The project structure provided here puts these functions in `utils.py` and then loads them as regular functions in `main.py`
add the following to `main.py`

```python
from utils import wifi_connect
print(wifi_connect("YOUR_SSID", "YOUR_PASSWORD"))
```
If you'd rather save the WiFi credentials on pico add the following to the existing `boot.py` on pico
```python
import network, time
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "PASSWORD")
for _ in range(10):
    if wlan.isconnected():
        break
    time.sleep(1)
print("Network config:", wlan.ifconfig())
```
## Useful Commands to know

#### Check freespace on Pico
```zsh
mpremote connect /dev/tty.usbmodem1401 fs df
```
#### List files
```zsh
mpremote connect /dev/tty.usbmodem1401 fs ls
```
### Raw REPL
```zsh
mpremote connect /dev/tty.usbmodem1401 repl
```
To exit REPL: `Ctrl-]`

## 9)Troubleshooting
* RPI-RP2 only → Replug to Mac-USB without BOOTSEL.

* No `/dev/tty.usbmodem*` exists
→ Make sure your cable supports data- and not only charging, try another port.

* system `pip/pip3` blocked → Use `pipx` from Homebrew (as above) or setup a virtualenvironment.
yaml.yml file included for minimum `venv` setup
* To Stop running scripts → `Ctrl-C` in REPL.
* to Exit screen → `Ctrl-A → Ctrl-\ → y`.

## 10) Basic Commands to work through python prompt
pico_repl_cheatsheet.pdf and pico_repl_FAQ.md included  in the project 
or you can put the following into your `main.py`
```python
# HEL and FAQ Sections
sections = [
    ("What is REPL?",
     "REPL stands for Read–Eval–Print–Loop. It is an interactive prompt where you can type Python commands and get immediate results."),

    ("Accessing REPL on macOS (Zsh)",
     "mpremote: mpremote connect /dev/tty.usbmodemXXXX\n"
     "screen: screen /dev/tty.usbmodemXXXX 115200\n"
     "Exit screen: Ctrl-A, then Ctrl-\\, then y"),

    ("Basic Commands",
     ">>> 2 + 3        # Math\n"
     ">>> print('Hi')  # Print text\n"
     ">>> help()       # Help menu\n"
     ">>> help('modules') # List modules"),

    ("Filesystem Commands",
     "import os\n"
     "os.listdir()                  # List files\n"
     "os.remove('file.py')           # Delete file\n"
     "os.rename('old.py', 'new.py')  # Rename file"),

    ("File Info & Storage",
     "import os\n"
     "for f in os.listdir():\n"
     "    print(f, os.stat(f)[6], 'bytes')\n"
     "stats = os.statvfs('/')\n"
     "total = stats[0] * stats[2]\n"
     "free = stats[0] * stats[3]\n"
     "print('Total:', total, 'Free:', free)"),

    ("Running Code from REPL",
     "exec(open('file.py').read())   # Run a script\n"
     "import mymodule                 # Import and run module code\n"
     "from mymodule import myfunc; myfunc()  # Run function"),

    ("Stopping Code",
     "Ctrl-C     # Stop running program in REPL\n"
     "Ctrl-D     # Soft reboot the Pico"),

    ("Tips",
     "- boot.py runs on startup (setup code)\n"
     "- main.py runs after boot.py (main program)\n"
     "- Use safe mode to bypass main.py if it locks up (hold BOOTSEL on reset for certain firmware modes)")
]
```

### @CyberAgSynBio Lab- 2025, Formatting and content revision credit ChatGPT o4-mini