# Pensum folders

Pensum folders for configuration and notes follow OS conventions.

You can get (but not set) those folders paths with `pm`:

```bash
# Notes folders
$ pm option get running.notes_folder
# Configuration folder
$ pm option get running.config_file
```

## GNU/Linux

- Notes : `~/.local/share/Pensum`.
- Configuration : `~/.config/Pensum`.

## macOS

- Notes : `~/Library/Application Support/Pensum`.
- Configuration : `~/Library/Preferences/Pensum`.

## Windows (7 and later)

- Notes : `C:\Users\USERNAME\AppData\Roaming\Pensum` or 
  `C:\Users\USERNAME\AppData\Local\Pensum`.
- Configuration : same as notes folder (!)

