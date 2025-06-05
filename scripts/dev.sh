#!/bin/bash

# Development script for resume project
# Opens the PDF and starts typst watch

# Change to the resume directory (parent of scripts) only if currently in scripts dir
if [[ "$(basename "$PWD")" == "scripts" ]]; then
    cd "$(dirname "$0")/.."
fi

# Open the PDF file in the default viewer (cross-platform)
echo "Opening will_cygan_resume.pdf..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open will_cygan_resume.pdf
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open will_cygan_resume.pdf
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash/MSYS2/Cygwin)
    start will_cygan_resume.pdf
else
    echo "Warning: Unknown OS type. Attempting to use xdg-open..."
    xdg-open will_cygan_resume.pdf 2>/dev/null || echo "Could not open PDF automatically"
fi

# Start typst watch in the foreground
echo "Starting typst watch..."
typst watch will_cygan_resume.typ