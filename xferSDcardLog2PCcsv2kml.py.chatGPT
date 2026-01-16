#!/usr/bin/env python3


import subprocess
import sys
from pathlib import Path

PICO_PORT = "/dev/ttyACM0"
REMOTE_FILE = "/sd/ultimateGPStrackerSDcard.log"
LOCAL_FILE  = "ultimateGPStrackerSDcard.log.OnPC.log"

def download_log():
    cmd = [
        "mpremote",
        "connect", PICO_PORT,
        "fs", "cp",
        f":{REMOTE_FILE}",
        LOCAL_FILE
    ]

    print("Downloading logfile from Pico...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR downloading file:")
        print(result.stderr)
        sys.exit(1)

    if not Path(LOCAL_FILE).exists():
        print("ERROR: File not created.")
        sys.exit(1)

    print("Download OK:", LOCAL_FILE)


if __name__ == "__main__":
    download_log()
