#!/usr/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
cd "$SCRIPT_DIR/../video-service"
source venv/bin/activate
python vlc_service.py
