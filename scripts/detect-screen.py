#!/usr/bin/env python3
import subprocess
import time
import socket
import sys
import argparse

from pathlib import Path
from PIL import Image
import imagehash

HASH_SIZE = 12

MONITOR_SOCKET = "./windows/windows-monitor.socket"
REFERENCE_PATH = "assets/lang-selection.png"
TEMP_SCREEN = "/tmp/vm-screen.ppm"

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)


def wait_for_monitor():
    while not Path(MONITOR_SOCKET).exists():
        time.sleep(0.5)
    sock.connect(MONITOR_SOCKET)


def get_screenshot(output_path: str):
    message = f"screendump {output_path}\n".encode()
    sock.sendall(message)
    time.sleep(0.1)
    return Image.open(output_path) if Path(output_path).exists() else None


def send_keys(keys: str):
    message = f"sendkey {keys}\n".encode()
    sock.sendall(message)


def start_vm():
    vm = subprocess.Popen(["quickemu", "--vm", "windows.conf"])
    wait_for_monitor()

    # Some new bug not sure why
    # reddit.com/r/qemu_kvm/comments/10rb28c/comment/jfms52h
    t = 0
    while True:
        t += 1
        time.sleep(0.5)
        send_keys("ret")
        if t > 10:
            break

    return vm


def capture_mode():
    print("Starting VM... Press 'S' when language selection screen appears")
    vm = start_vm()

    while input("Press 'S' to capture: ").strip().upper() != "S":
        pass

    Path("assets").mkdir(exist_ok=True)
    img = get_screenshot(TEMP_SCREEN)
    if img is None:
        return

    img.save(REFERENCE_PATH, "PNG", optimize=True)

    print(f"Saved screen to {REFERENCE_PATH}")
    vm.terminate()


def automate_mode():
    if not Path(REFERENCE_PATH).exists():
        sys.exit(f"Error: {REFERENCE_PATH} not found. Run 'capture' first.")

    ref_hash = imagehash.phash(Image.open(REFERENCE_PATH), hash_size=HASH_SIZE)
    # print(ref_hash)

    vm = start_vm()

    print("Monitoring for language screen...")
    try:
        while True:
            time.sleep(2)
            img = get_screenshot(TEMP_SCREEN)
            if not img:
                continue

            new_hash = imagehash.phash(img, hash_size=HASH_SIZE)
            print(new_hash)
            distance = new_hash - ref_hash
            print(f"Distance: {distance}  ", end="\r")

            if distance < 5:
                print("\n✓ Detected! Sending Alt+N...")
                send_keys("alt-n")
                break
        _ = vm.wait()
    except KeyboardInterrupt:
        vm.terminate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("command", choices=["capture", "automate"])
    args = parser.parse_args()

    if args.command == "capture":
        capture_mode()
    else:
        automate_mode()
