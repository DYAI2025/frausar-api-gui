-- Test script for custom shortcut
tell application "Terminal"
    activate
    do script "cd \"" & (do shell script "pwd") & "\""
end tell