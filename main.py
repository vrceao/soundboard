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
keybinds = preferences["keybinds"]

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
        print("ERROR Log file somehow disappeared")
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
    if log_sounds:
        log(path);

    if not allow_overlap:
        # Todo: kill other instances
        pass

    print(f"Playing {path.split("/")[-1]}")

    subprocess.Popen(
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

# Todo: make this work, kill all other instances
def stop():
    return

def on_key(e):
    if e.event_type != "down":
        return

    if e.name not in keybinds:
        return

    if keybinds[e.name] == stop_key:
        stop()
        return

    play(sounds_dir + keybinds[e.name] if sounds_dir.endswith("/") else sounds_dir + "/" + keybinds[e.name])

keyboard.hook(on_key)

if log_sounds:
    init_log()

keyboard.wait()