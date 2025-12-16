# Bloxwrapper

<p align="center">
  <video src="https://raw.githubusercontent.com/Bloxwrapper/Bloxwrapper/main/example.mp4" controls style="max-width:100%;height:auto;">
    Your browser does not support the video tag. You can download or view the example directly:
    <a href="https://raw.githubusercontent.com/Bloxwrapper/Bloxwrapper/main/example.mp4">example.mp4</a>
  </video>
</p>

**Bloxwrapper** (`bwrap`) is a command-line tool that converts any Roblox game into a Windows executable with a fully embedded Roblox client. It uses **PyQt5** to create a windowed wrapper and allo[...]

---

## What is Bloxwrapper?

Bloxwrapper is a Roblox wrapper generator that:

- Launches a Roblox game via its **Place ID**.
- Shows a **loading message** until the Roblox client is fully loaded.
- **Embeds the Roblox client** directly into a PyQt5 window.
- Allows customization of the **EXE icon** and **window title**.
- Generates a **ready-to-run executable** (non-onefile) for Windows.

It’s ideal for distributing Roblox games as standalone executables while keeping the Roblox client embedded.

---

## Features

- Command-line interface for generating Roblox wrappers.
- Support for custom **icons** (`.png` or `.ico`) for both the EXE and PyQt5 window.
- Custom **window title** for your wrapper.
- Automatically embeds Roblox once the client launches.
- Generates a non-onefile EXE with all dependencies included for reliable execution.

---

## Usage

```bash
# Basic usage
bwrap <placeId>

# With custom output folder
bwrap 194184689 output=MyGame

# With custom icon and window title
bwrap 194184689 output=MyGame icon=cliicon.png title="My Roblox Game"
```

