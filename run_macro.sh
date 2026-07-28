#!/bin/bash
# ==============================================================================
# Macbook to Secondary Display Macro Background Runner
# Runs the recorded CrossMacro file (/Users/ganidhu/Documents/MacbookTo2ndaryDisp_Working1.macro)
# silently in the background and exits immediately.
# ==============================================================================

MACRO_PATH="/Users/ganidhu/Documents/MacbookTo2ndaryDisp_Working1.macro"
CROSSMACRO_BIN="/Applications/CrossMacro.app/Contents/MacOS/CrossMacro.UI"

if [ ! -f "$MACRO_PATH" ]; then
    echo "Error: Macro file not found at $MACRO_PATH" >&2
    exit 1
fi

if [ ! -x "$CROSSMACRO_BIN" ]; then
    echo "Error: CrossMacro executable not found at $CROSSMACRO_BIN" >&2
    exit 1
fi

# Run playback in the background detached from the shell
nohup "$CROSSMACRO_BIN" play "$MACRO_PATH" "$@" > /dev/null 2>&1 &

echo "Macro triggered in background (PID: $!). Exiting runner."
exit 0
