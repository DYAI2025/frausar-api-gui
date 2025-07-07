#!/usr/bin/osascript
tell application "Terminal"
    activate
    do script "cd \"" & (do shell script "pwd") & "\""
end tell