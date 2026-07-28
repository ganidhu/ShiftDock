#!/bin/bash
# ==============================================================================
# ShiftDock Recorder Script
# Records a macro via CrossMacro CLI and saves it to specified output file
# ==============================================================================

DEFAULT_OUTPUT="/Users/ganidhu/Documents/MacbookTo2ndaryDisp_Working1.macro"
CROSSMACRO_BIN="/Applications/CrossMacro.app/Contents/MacOS/CrossMacro.UI"

OUTPUT_FILE="${1:-$DEFAULT_OUTPUT}"
shift 1 2>/dev/null

if [ ! -x "$CROSSMACRO_BIN" ]; then
    echo "Error: CrossMacro executable not found at $CROSSMACRO_BIN" >&2
    exit 1
fi

echo "======================================================"
echo " ⏺️  ShiftDock Macro Recorder"
echo "======================================================"
echo " Output file: $OUTPUT_FILE"
echo " Recording started! Press Ctrl+C in terminal or wait for duration to stop."
echo "======================================================"

"$CROSSMACRO_BIN" record -o "$OUTPUT_FILE" "$@"
