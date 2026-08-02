import keyboard
import subprocess
import json
import json5
import time
from datetime import datetime
import os

with open("preferences.jsonc", "r", encoding="utf-8") as f:
    preferences = json5.load(f)

sounds_dir = preferences["sounds_dir"]
stop_key = preferences["stop_key"]
volume_percentage = preferences["volume_percentage"]
log_sounds = preferences["log_sounds"]
allow_overlap = preferences["allow_overlap"]
allow_hold = preferences["allow_hold"]
keybinds = preferences["keybinds"]

current_sounds = []
keys_held = []

def message(text):
    print(f"{get_date()} {text}")

def get_date():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def get_unix():
    return str(time.time()).split(".")[0]

log_file = f"logs/{get_date()}.json"

def init_log():
    os.makedirs("logs", exist_ok=True)

    with open(log_file, "w", encoding="utf-8") as f:
            json5.dump([], f, indent=4)

def log(path):
    if not os.path.exists(log_file):
        message("ERROR Log file somehow disappeared")
        init_log()

    with open(log_file, "r", encoding="utf-8") as f:
        logs = json5.load(f)

    logs.append({
        "timestamp": get_unix(),
        "sound": path.split("/")[-1]
    })

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

def play(path):
    global current_sounds

    current_sounds = [
        sound for sound in current_sounds
        if sound.poll() is None
    ]

    if log_sounds:
        log(path);

    if not allow_overlap:
        stop()

    message(f"Playing {path.split("/")[-1]}")

    sound = subprocess.Popen(
        [
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-volume", str(volume_percentage),
            path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    current_sounds.append(sound)

def stop():
    global current_sounds

    message("Stopping all sounds")

    for sound in current_sounds:
        sound.kill()

    current_sounds.clear()

def on_key(e):
    global keys_held

    key = e.name

    if e.event_type != "down":
        if key in keys_held:
            keys_held.remove(key)
        return

    if key == stop_key:
        stop()
        return

    if not allow_hold:
        if key in keys_held:
            return

    keys_held.append(key)

    mods = []

    if "shift" in keys_held:
        mods.append("shift")
    if "alt" in keys_held:
        mods.append("alt")
    if "ctrl" in keys_held:
        mods.append("ctrl")

    if key not in keybinds:
        return

    play(os.path.join(sounds_dir, keybinds[key]))

def helper_error(var, type):
    string = None

    if type == "str":
        string = "should be a string, put it in quotes"
    elif type == "bool":
        string = "should be a boolean, enter either true or false, don't capitalize the first character"
    elif type == "vol":
        string = "should be either an integer, float or a string. Just put a number from 0 to 100, it's really not that hard"
    message(f"ERROR {var} {string}")

if not isinstance(sounds_dir, str):
    helper_error("sounds_dir", "str")
if not isinstance(stop_key, str):
    helper_error("stop_key", "str")
if not isinstance(volume_percentage, (int, float, str)):
    helper_error("volume_percentage", "vol")
if not isinstance(log_sounds, bool):
    helper_error("log_sounds", "bool")
if not isinstance(allow_overlap, bool):
    helper_error("allow_overlap", "bool")
if not isinstance(allow_hold, bool):
    helper_error("allow_hold", "bool")

keyboard.hook(on_key)

if log_sounds:
    init_log()

keyboard.wait()