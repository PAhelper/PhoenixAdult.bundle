# Watchdog Adult Renamer
Using [Metadata API](http://metadataapi.net/) for renaming files

---

# How to use
1. Make sure you have installed Python 3.4 or higher
2. Run `pip install -r requirements.txt` to install all dependency
3. Run main.py

```
usage: main.py -i INPUT_PATH -o OUTPUT_PATH [-c] [-a]

Watchdog Adult Renamer.

optional arguments:
  -i INPUT_PATH, --input_path INPUT_PATH
                        Directory to watch files
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Directory to store renamed files
  -c, --cleanup         Remove metadata title from file
  -a, --additional_info
                        Add additional info to filename
```

# Note
I can't guarantee 100% accuracy. Use it on your risk.
