import sys
import os
import subprocess
import textwrap

def parse_args():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)

    place_id = sys.argv[1]
    output = "BloxwrapperGame"
    icon = None
    title = "Bloxwrapper"

    for arg in sys.argv[2:]:
        if arg.startswith("output="):
            output = arg.split("=", 1)[1]
        elif arg.startswith("icon="):
            icon = arg.split("=", 1)[1]
        elif arg.startswith("title="):
            title = arg.split("=", 1)[1]

    return place_id, output, icon, title

def print_usage():
    usage_text = """
Bloxwrapper v1.0, By Zohan Haque, "ZohanHaqueOffical" for Roblox

Usage:
    bwrap <placeId> [options]

Required:
    <placeId>           Roblox Place ID to wrap

Options:
    output=<folder>     Output folder and EXE name (default: BloxwrapperGame)
    icon=<file>         Path to an icon file (PNG or ICO) for the EXE and window
    title=<title>       Custom window title (default: "Bloxwrapper")

Examples:
    bwrap 194184689
    bwrap 194184689 output=MyGame
    bwrap 194184689 output=MyGame icon=icon.png title="My Roblox Game"
"""
    print(usage_text)

PLACE_ID, OUTPUT, ICON, TITLE = parse_args()

os.makedirs(OUTPUT, exist_ok=True)

WRAPPER_FILE = os.path.join(OUTPUT, "wrapper.py")

# Full path to icon (if provided)
ICON_PATH = None
if ICON:
    ICON_PATH = os.path.abspath(ICON)
    if not os.path.exists(ICON_PATH):
        print(f"[!] Icon '{ICON}' not found, continuing without icon.")
        ICON_PATH = None

# -----------------------------
# GENERATED WRAPPER SOURCE
# -----------------------------
wrapper_code = f"""
import sys
import subprocess
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel
import win32gui
import win32con

PLACE_ID = "{PLACE_ID}"

class RobloxWrapper(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("{TITLE}")
        self.setGeometry(200, 200, 1280, 720)

        # Set PyQt window icon if provided
        {'from PyQt5.QtGui import QIcon\n        self.setWindowIcon(QIcon(r"' + ICON_PATH + '"))' if ICON_PATH else ''}

        self.label = QLabel("Loading...", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(self.label)

        self.roblox_hwnd = None
        subprocess.Popen(f'start "" "roblox://placeId={{PLACE_ID}}"', shell=True)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.find_roblox)
        self.timer.start(500)

    def find_roblox(self):
        def enum(hwnd, _):
            title = win32gui.GetWindowText(hwnd)
            if "Roblox" in title:
                self.roblox_hwnd = hwnd
                return False
            return True

        win32gui.EnumWindows(enum, None)

        if self.roblox_hwnd:
            self.timer.stop()
            self.embed()

    def embed(self):
        win32gui.SetParent(self.roblox_hwnd, int(self.winId()))
        win32gui.SetWindowLong(
            self.roblox_hwnd,
            win32con.GWL_STYLE,
            win32con.WS_VISIBLE
        )
        self.label.hide()
        self.resizeEvent(None)

    def resizeEvent(self, event):
        if self.roblox_hwnd:
            win32gui.MoveWindow(
                self.roblox_hwnd,
                0, 0,
                self.width(),
                self.height(),
                True
            )

app = QtWidgets.QApplication(sys.argv)
win = RobloxWrapper()
win.show()
sys.exit(app.exec_())
"""

with open(WRAPPER_FILE, "w", encoding="utf-8") as f:
    f.write(textwrap.dedent(wrapper_code))

print("[+] Wrapper source created")

# -----------------------------
# BUILD EXE AUTOMATICALLY
# -----------------------------

cmd = [
    "pyinstaller",
    "--noconfirm",
    "--windowed",
    "--name", OUTPUT,
]

if ICON_PATH:
    cmd.append(f"--icon={ICON_PATH}")

cmd.append("wrapper.py")

print("[*] Building EXE...")
subprocess.run(
    cmd,
    cwd=OUTPUT,
    shell=True
)

print(f"[✔] Compile Finished. EXE is in {OUTPUT}/dist/{OUTPUT}/")
