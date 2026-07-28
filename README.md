# ShiftDock 🚀

> Zero-GUI background macro trigger & interactive CLI runner for macOS — powered by CrossMacro.

---

## 🧠 The Problem ShiftDock Solves: macOS Multi-Display Dock Trapping

### The Geometry Issue with Vertically Stacked Displays
On macOS, when using **Displays Have Separate Spaces**, the Dock is designed to follow your cursor to whatever monitor you are actively using. To summon the Dock onto a specific screen, macOS listens for cursor **"edge pressure" or "dwelling"** against the bottom edge of that monitor.

However, in vertically stacked arrangements — such as an **External Monitor positioned directly above a notched MacBook**:

```
        ┌──────────────────────────────────┐
        │     External Display (Top)       │
        └──────────────────────────────────┘
                         │ (Shared Seam)
        ┌──────────────────────────────────┐
        │  MacBook Display (with Notch)    │
        └──────────────────────────────────┘
```

### Why Cursor Dock Movement Breaks:
1. **Shared Seam vs. Exposed Edge**: The bottom boundary of the top external monitor is a **shared screen seam**, not an outer physical boundary. When you try to summon the Dock on the top monitor by dragging your cursor down, **the cursor simply slips across the seam into the MacBook display below** instead of pressing against an edge.
2. **Dock Trapping on the Lower Screen**: Because the MacBook screen is at the bottom, its bottom edge is an actual outer boundary. The Dock gets permanently trapped on the MacBook display, making it virtually impossible to summon it back up to the top external display through normal mouse movement.

### ⚡ How ShiftDock Fixes It:
**ShiftDock** bypasses macOS's flawed edge-pressure detection entirely. By binding a recorded macro or hotkey to CrossMacro's headless engine, ShiftDock instantly moves your cursor and summons the Dock to your secondary/top display via a background CLI call or hotkey app, with zero mouse thrashing.

---

## 📦 Installation

From this folder:

```bash
./install.sh
```

Or manually:

```bash
# pipx (recommended)
pipx install .

# or editable with pip
pip3 install -e . --break-system-packages
```

Then from anywhere:

```bash
shiftdock
```

---

## 🚀 Usage

### Interactive Pipeline (default)

Simply type:

```bash
shiftdock
```

Walks you through:
1. **▶️ Run default macro in background** (`MacbookTo2ndaryDisp_Working1.macro`)
2. **📂 Pick & run custom `.macro` file** (using native macOS file picker)
3. **⏺️ Record a new macro**
4. **🍎 Convert `.macro` file to a standalone macOS `.app` bundle**
5. **ℹ️ Inspect macro details**
6. **🩺 Run system diagnostics**

### One-Shot CLI

```bash
# Run macro headlessly in background
shiftdock run

# Run macro with custom speed & repeat count
shiftdock run ~/Documents/MyMacro.macro --speed 1.5 --repeat 3

# Convert any .macro into a standalone macOS App!
shiftdock app ~/Documents/MyMacro.macro

# Record a new macro (press Ctrl+C in terminal when done)
shiftdock record ~/Documents/MyNewMacro.macro

# Record a macro with 10-second auto-stop duration
shiftdock record ~/Documents/MyNewMacro.macro --duration 10
```

### Meta Commands

```bash
shiftdock --help
shiftdock --about
shiftdock --version
shiftdock doctor
```

---

## 🍎 Macro → macOS `.app` Converter

ShiftDock can instantly compile any recorded `.macro` file into a standalone macOS `.app` bundle:

```bash
shiftdock app ~/Documents/Custom1.macro
```

Or choose Option `4` in the interactive TUI. The resulting `.app` is compiled to `/Applications`, allowing you to trigger your background macros directly from **Spotlight**, **Raycast**, **Alfred**, **Launchpad**, or your **Dock**!

---

## 📄 License
MIT License
