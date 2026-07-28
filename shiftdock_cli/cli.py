#!/usr/bin/env python3
"""Interactive CLI for ShiftDock (sprite-separator / wav-fourier-chladni style TUI)."""

import os
import sys
import time
import shutil
import subprocess
import platform
from pathlib import Path

__version__ = "1.2.0"

CLEAR = "\033[2J\033[H"
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
DIM = "\033[2m"
WHITE = "\033[37m"

CMD_NAME = "shiftdock"
CROSSMACRO_BIN = "/Applications/CrossMacro.app/Contents/MacOS/CrossMacro.UI"
DEFAULT_MACRO = os.path.expanduser("~/Documents/MacbookTo2ndaryDisp_Working1.macro")
FIRST_RUN_FLAG = os.path.expanduser("~/.shiftdock_first_run_done")


def is_first_run() -> bool:
    return not os.path.exists(FIRST_RUN_FLAG)


def mark_first_run_done():
    Path(FIRST_RUN_FLAG).touch()


def banner(subtitle: str = "Background Macro Automation") -> None:
    print(f"{BOLD}{GREEN}┌────────────────────────────────────────────────────────┐{RESET}")
    title = f"SHIFTDOCK · {subtitle}"
    pad = max(0, 54 - len(title))
    print(f"{BOLD}{GREEN}│  {title}{' ' * pad}│{RESET}")
    print(f"{BOLD}{GREEN}└────────────────────────────────────────────────────────┘{RESET}")
    print()


def animate_loader(stage_name: str, frames=None, loops: int = 2, delay: float = 0.08) -> None:
    frames = frames or ["✻", "✳", "·"]
    for _ in range(loops):
        for char in frames:
            print(f"\r  {CYAN}{char} {stage_name}{RESET}", end="", flush=True)
            time.sleep(delay)
    print("\r" + " " * (len(stage_name) + 10) + "\r", end="", flush=True)


def get_macro_picker_mac() -> str | None:
    script = (
        'tell application (path to frontmost application as text)\n'
        'set theFile to choose file with prompt "Select a CrossMacro file (.macro):" '
        'of type {"public.data", "public.item"}\n'
        "POSIX path of theFile\n"
        "end tell"
    )
    try:
        proc = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=120,
        )
        path = proc.stdout.strip()
        if path:
            return path
    except Exception:
        pass
    return None


def print_guidance(action: str) -> None:
    """Print contextual first-run guidance for a given action."""
    print()
    if action == "run":
        print(f"  {YELLOW}Note:{RESET} On first use, macOS may show a permission popup.")
        print(f"  {DIM}Allow 'Accessibility' and 'Input Monitoring' access when prompted.{RESET}")
        print(f"  {DIM}This lets CrossMacro move your mouse and replay keyboard inputs.{RESET}")
    elif action == "record":
        print(f"  {YELLOW}Note:{RESET} On first use, macOS may ask for 'Input Monitoring' permission.")
        print(f"  {DIM}Allow it in System Settings → Privacy & Security → Input Monitoring.{RESET}")
        print(f"  {DIM}This lets CrossMacro listen to your mouse and keyboard while recording.{RESET}")
    elif action == "build_app":
        print(f"  {YELLOW}Note:{RESET} The compiled .app will appear in /Applications.")
        print(f"  {DIM}On first launch of that app, macOS may ask you to confirm opening it.{RESET}")
        print(f"  {DIM}Right-click → Open if macOS blocks it for being from an 'unidentified developer'.{RESET}")
    print()


def handle_about() -> None:
    print(CLEAR)
    banner("About")
    print(f"  {BOLD}ShiftDock v{__version__}{RESET}")
    print("  Zero-GUI background macro trigger & interactive CLI runner for macOS.")
    print("\n  • Solves macOS Dock trapping across vertically stacked monitor seams")
    print("  • Triggers recorded CrossMacro automation headlessly in the background")
    print("  • Native macOS file pickers + interactive step-by-step TUI")
    print("  • Macro → Standalone macOS .app Converter (`shiftdock app <file>`)")
    print("  • Global CLI + optional macOS .app launcher support")
    x_link = "\033]8;;https://x.com/ItzGanidhu\033\\[@X]\033]8;;\033\\"
    gh_link = "\033]8;;https://github.com/ganidhu\033\\[@GitHub]\033]8;;\033\\"
    print(f"\n  {BOLD}Author:{RESET} ganidhu {x_link} {gh_link}")
    print(f"  {BOLD}License:{RESET} MIT\n")
    sys.exit(0)


def handle_help() -> None:
    print(f"\n  {BOLD}{CMD_NAME}{RESET} — macOS Zero-GUI Background Macro Trigger & App Converter")
    print(f"\n  {CYAN}Usage:{RESET}")
    print(f"    {CMD_NAME}                 Launch the interactive pipeline")
    print(f"    {CMD_NAME} run             Run default macro in background")
    print(f"    {CMD_NAME} run <macro>     Run specific .macro file in background")
    print(f"    {CMD_NAME} record [file]   Record a new macro via CLI")
    print(f"    {CMD_NAME} app [macro]     Compile .macro into a standalone macOS .app bundle")
    print(f"    {CMD_NAME} info [file]     Inspect macro details & breakdown")
    print(f"    {CMD_NAME} doctor          Check permissions & dependencies")
    print(f"    {CMD_NAME} --about         Show project info")
    print(f"    {CMD_NAME} --update        Upgrade / reinstall via install.sh")
    print(f"    {CMD_NAME} --uninstall     Remove the package via pipx")
    print(f"    {CMD_NAME} --help          Show this help message")
    print(f"\n  {CYAN}Quick Examples:{RESET}")
    print(f"    {CMD_NAME} app ~/Documents/MyMacro.macro")
    print(f"    {CMD_NAME} run --speed 1.5 --repeat 2")
    print(f"    {CMD_NAME} record ~/Documents/Custom1.macro --duration 10\n")
    sys.exit(0)


def handle_update() -> None:
    print(CLEAR)
    banner("Update")
    script_path = Path(__file__).resolve().parent.parent / "install.sh"
    if script_path.exists():
        print(f"  {CYAN}Re-running installer from {script_path}…{RESET}\n")
        subprocess.run(["bash", str(script_path)])
    else:
        print(f"  {CYAN}Updating via pipx…{RESET}\n")
        subprocess.run(["pipx", "reinstall", "shiftdock"])
    sys.exit(0)


def handle_uninstall() -> None:
    print(CLEAR)
    banner("Uninstall")
    print(f"  {YELLOW}Removing ShiftDock via pipx…{RESET}\n")
    subprocess.run(["pipx", "uninstall", "shiftdock"])
    sys.exit(0)


def cmd_create_app(macro_path: str = DEFAULT_MACRO, app_name: str | None = None, out_dir: str = "/Applications"):
    if not os.path.exists(macro_path):
        print(f"  {RED}Error: Macro file not found at {macro_path}{RESET}")
        sys.exit(1)

    macro_path = os.path.abspath(macro_path)
    stem = Path(macro_path).stem.replace("_Working1", "").replace("_", "")
    name = app_name or stem or "ShiftDockMacro"
    app_filename = name if name.endswith(".app") else f"{name}.app"
    target_app_path = os.path.join(out_dir, app_filename)

    if is_first_run():
        print_guidance("build_app")

    animate_loader(f"Compiling standalone macOS bundle '{app_filename}'...")

    applescript = f'do shell script "{CROSSMACRO_BIN} play \\"{macro_path}\\" > /dev/null 2>&1 &"'

    try:
        subprocess.run(
            ["osacompile", "-o", target_app_path, "-e", applescript],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        png_asset = Path(__file__).resolve().parent.parent / "ASSETS" / "app_icon.png"
        icns_asset = Path(__file__).resolve().parent.parent / "ASSETS" / "app_icon.icns"
        if icns_asset.exists():
            target_res = Path(target_app_path) / "Contents" / "Resources"
            if target_res.exists():
                shutil.copy(icns_asset, target_res / "applet.icns")
        
        if png_asset.exists():
            set_icon_script = f'''
            use framework "AppKit"
            use scripting additions
            set iconPath to "{png_asset}"
            set appPath to "{target_app_path}"
            set theIcon to current application's NSImage's alloc()'s initWithContentsOfFile:iconPath
            (current application's NSWorkspace's sharedWorkspace()'s setIcon:theIcon forFile:appPath options:0)
            '''
            subprocess.run(["osascript", "-e", set_icon_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"  {BOLD}{GREEN}✓ App compiled successfully!{RESET}")
        print(f"  Location: {YELLOW}{target_app_path}{RESET}")
        print(f"  {DIM}Launch via Spotlight, Finder, Raycast, or your Dock.{RESET}\n")
    except Exception as e:
        print(f"  {RED}Failed to compile app bundle: {e}{RESET}\n")


def run_pipeline():
    first = is_first_run()

    print(CLEAR, end="")
    banner("Interactive Pipeline")

    macro_name = os.path.basename(DEFAULT_MACRO)
    print(f"  {DIM}Default macro:{RESET} {macro_name}\n")

    # Menu
    col = 14
    print(f"  {CYAN}[1]{RESET} {'run':<{col}}{DIM}Play the default macro in the background{RESET}")
    print(f"  {CYAN}[2]{RESET} {'run file':<{col}}{DIM}Pick and run any .macro file{RESET}")
    print()
    print(f"  {CYAN}[3]{RESET} {'record':<{col}}{DIM}Record new mouse/keyboard actions to a macro{RESET}")
    print(f"  {CYAN}[4]{RESET} {'build app':<{col}}{DIM}Compile a .macro into a standalone macOS .app{RESET}")
    print()
    print(f"  {CYAN}[5]{RESET} {'info':<{col}}{DIM}Show macro event breakdown & metadata{RESET}")
    print(f"  {CYAN}[6]{RESET} {'doctor':<{col}}{DIM}Check permissions & dependencies{RESET}")
    print(f"  {CYAN}[0]{RESET} {'exit':<{col}}")
    print()

    choice = input(f"  {BOLD}›{RESET} ").strip()

    if choice == "1":
        if first:
            print_guidance("run")
            mark_first_run_done()
        cmd_run(DEFAULT_MACRO)
    elif choice == "2":
        path = get_macro_picker_mac() if platform.system() == "Darwin" else input("  Enter macro path: ").strip()
        if path and os.path.exists(path):
            if first:
                print_guidance("run")
                mark_first_run_done()
            cmd_run(path)
        else:
            print(f"\n  {RED}Invalid file or action cancelled.{RESET}")
    elif choice == "3":
        if first:
            print_guidance("record")
            mark_first_run_done()
        default_rec = os.path.expanduser("~/Documents/Custom1.macro")
        out_file = input(f"\n  Save macro to [{default_rec}]: ").strip() or default_rec
        cmd_record(out_file)
    elif choice == "4":
        path = get_macro_picker_mac() if platform.system() == "Darwin" else DEFAULT_MACRO
        if path and os.path.exists(path):
            suggested = Path(path).stem.replace("_Working1", "")
            app_name = input(f"  App Name [{suggested}]: ").strip() or suggested
            cmd_create_app(path, app_name=app_name)
            if first:
                mark_first_run_done()
        else:
            print(f"\n  {RED}Invalid macro file or action cancelled.{RESET}")
    elif choice == "5":
        path = get_macro_picker_mac() if platform.system() == "Darwin" else DEFAULT_MACRO
        if path:
            cmd_info(path)
    elif choice == "6":
        cmd_doctor()
    else:
        print(f"\n  {YELLOW}Goodbye!{RESET}\n")


def cmd_run(macro_path: str = DEFAULT_MACRO, speed: float = 1.0, repeat: int = 1):
    if not os.path.exists(macro_path):
        print(f"  {RED}Error: Macro file not found at {macro_path}{RESET}")
        sys.exit(1)

    if not os.path.exists(CROSSMACRO_BIN):
        print(f"  {RED}Error: CrossMacro executable not found at {CROSSMACRO_BIN}{RESET}")
        sys.exit(1)

    animate_loader("Launching macro headlessly in background...")

    args = [CROSSMACRO_BIN, "play", macro_path]
    if speed != 1.0:
        args.extend(["--speed", str(speed)])
    if repeat > 1:
        args.extend(["--repeat", str(repeat)])

    proc = subprocess.Popen(
        args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setpgrp
    )

    print(f"  {BOLD}{GREEN}✓ Macro triggered in background!{RESET} {DIM}(PID: {proc.pid}){RESET}\n")


def cmd_record(output_path: str = DEFAULT_MACRO, duration: int = 0):
    if not os.path.exists(CROSSMACRO_BIN):
        print(f"  {RED}Error: CrossMacro executable not found at {CROSSMACRO_BIN}{RESET}")
        sys.exit(1)

    print(f"\n  {BOLD}{CYAN}Recording Macro{RESET}")
    print(f"  Output: {YELLOW}{output_path}{RESET}")
    print(f"  {DIM}Press Ctrl+C in terminal when finished.{RESET}\n")

    args = [CROSSMACRO_BIN, "record", "-o", output_path]
    if duration > 0:
        args.extend(["--duration", str(duration)])

    try:
        subprocess.run(args)
        print(f"\n  {BOLD}{GREEN}✓ Recording saved to {output_path}!{RESET}\n")
    except KeyboardInterrupt:
        print(f"\n  {BOLD}{GREEN}✓ Recording stopped and saved!{RESET}\n")


def cmd_info(macro_path: str = DEFAULT_MACRO):
    if not os.path.exists(CROSSMACRO_BIN):
        print(f"  {RED}Error: CrossMacro binary not found.{RESET}")
        sys.exit(1)

    print(f"\n  {BOLD}Macro Information:{RESET}\n")
    subprocess.run([CROSSMACRO_BIN, "macro", "info", macro_path])
    print()


def cmd_doctor():
    if not os.path.exists(CROSSMACRO_BIN):
        print(f"  {RED}Error: CrossMacro binary not found.{RESET}")
        sys.exit(1)

    print(f"\n  {BOLD}System Health & Diagnostics:{RESET}\n")
    subprocess.run([CROSSMACRO_BIN, "doctor"])
    print()


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)

    if argv:
        arg = argv[0].lower()
        if arg in ["--uninstall", "-uninstall", "uninstall"]:
            handle_uninstall()
        elif arg in ["--update", "-update", "update"]:
            handle_update()
        elif arg in ["--about", "-about", "about"]:
            handle_about()
        elif arg in ["--help", "-help", "help", "-h"]:
            handle_help()
        elif arg in ["run", "play"]:
            target = argv[1] if len(argv) > 1 and not argv[1].startswith("-") else DEFAULT_MACRO
            if is_first_run():
                print_guidance("run")
                mark_first_run_done()
            cmd_run(target)
            return
        elif arg in ["app", "convert", "build-app"]:
            target = DEFAULT_MACRO
            app_name = None
            for i, a in enumerate(argv[1:], 1):
                if a in ["--name", "-n"] and i + 1 < len(argv):
                    app_name = argv[i + 1]
                elif not a.startswith("-") and (i == 1 or argv[i - 1] not in ["--name", "-n"]):
                    target = a
            cmd_create_app(target, app_name=app_name)
            return
        elif arg in ["record", "rec"]:
            target = argv[1] if len(argv) > 1 and not argv[1].startswith("-") else os.path.expanduser("~/Documents/Custom1.macro")
            if is_first_run():
                print_guidance("record")
                mark_first_run_done()
            cmd_record(target)
            return
        elif arg in ["info", "validate"]:
            target = argv[1] if len(argv) > 1 and not argv[1].startswith("-") else DEFAULT_MACRO
            cmd_info(target)
            return
        elif arg in ["doctor", "check"]:
            cmd_doctor()
            return
        else:
            print(f"\n  Unknown option: {argv[0]}")
            print("  Available: --help, --about, --update, --uninstall")
            print(f"  Or: {CMD_NAME} [run|record|app|info|doctor]\n")
            sys.exit(1)

    try:
        run_pipeline()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Goodbye!{RESET}\n")


if __name__ == "__main__":
    main()
