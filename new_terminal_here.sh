#!/bin/bash
# Script to open new terminal in current directory
osascript -e 'tell application "Terminal" to do script "cd \"$(pwd)\""'