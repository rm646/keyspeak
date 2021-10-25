
Thanks to https://stackoverflow.com/a/61674334

# Prerequisites and setup

Install VB-CABLE from https://vb-audio.com/Cable/
Set device names for mic and speakers (use print_devices.py to list their names)

# generate_sounds

To generate mp3 files, use the generate_sounds.py script. You can
just provide the output filename and this will be used as the text
to speak.

```
Usage: python generate_sounds.py [OPTIONS]

  Generates a spoken mp3 file of the given text

Options:
  -o, --output TEXT  Output filename  [required]
  -t, --text TEXT    Text to convert to speech
  -l, --lang TEXT    Language to pass to gTTS, default English
  --help             Show this message and exit.

```

## Example
```
Example:

python generate_sounds.py -o hello

```

# keyspeak

You'll need to set the SPEAKER_DEVICE_NAME and MIC_DEVICE_NAME for your
setup. Use print_devices.py to list what's available.