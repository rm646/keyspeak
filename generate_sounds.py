import click
import os

from gtts import gTTS

@click.command()
@click.option('-o', '--output', required=True, help='Output filename')
@click.option('-t', '--text', help='Text to convert to speech')
@click.option('-l', '--lang', default='en', help='Language to pass to gTTS, default English')
def generate_sound_file(output, text, lang):
    """Generates a spoken mp3 file of the given text"""
    if not text:
        text = output  # use filename if no text given
    myobj = gTTS(text=text, lang=lang, slow=False)
    myobj.save(f"{output}.mp3")

if __name__ == '__main__':
    generate_sound_file()