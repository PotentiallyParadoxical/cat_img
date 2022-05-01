#!/usr/bin/env python
import io, sys, subprocess, os
import textwrap, re, random

from PIL import Image, ImageDraw, ImageFont
import requests

def build_cat_image():
    fortune_options = ['computers', '-s']

    def get_cat_img() -> Image.Image:
        # Get an image of a cat from public internet cat generating robo slave
        # To add offline mode, might add capabilities to grab from local files instead
        url = 'https://thiscatdoesnotexist.com/'
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content))

    def get_fortune() -> str:
        # Run fortune and grab the stdout(output) and get output in text and return it
        result = subprocess.run(
            ['fortune'] + fortune_options, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')

    def owo_text(text: str) -> str:
        # Based off of https://github.com/zuzak/owo
        substitutions = {
            'r': 'w',
            'l': 'w',
            'R': 'W',
            'L': 'W',
            'no': 'nu',
            'has': 'haz',
            'have': 'haz',
            ' says': ' sez',
            'you': 'uu',
            'the ': 'da ',
            'The ': 'Da ',
            'THE ': 'DA '
        }
        prefixes = [ '<3 ', '0w0 ', 'H-hewwo?? ', 'HIIII! ', 'Haiiii! ', 'Huohhhh. ', 'OWO ', 'OwO ', 'UwU ']
        suffixes = [
            ' (;w;)', ' ._.', ' :3', ' :3c', ' :D', ' :O', ' :P', ' ;-;', ' ;3', ' ;_;', 
            ' <{^v^}>', ' >_<', ' >_>', ' UwU', ' XDDD',' ^-^', ' ^_^', 
            ' x3', ' x3', ' xD', 'fwendo'
        ]

        for sub in substitutions:
            text = text.replace(sub, substitutions[sub])
        text = random.choice(prefixes) + text + random.choice(suffixes)
        return text

    def write_text_on_draw(draw: ImageDraw.ImageDraw, text: str):
        def draw_with_border(text, xy, text_color, outline_color):
            x, y = xy
            # Text Outline Cardinal
            draw.text((x-1, y), text=text, fill=outline_color, font=font)
            draw.text((x+1, y), text=text, fill=outline_color, font=font)
            draw.text((x, y-1), text=text, fill=outline_color, font=font)
            draw.text((x, y+1), text=text, fill=outline_color, font=font)
            # Text Outline Diagonal
            draw.text((x-1, y-1), text=text, fill=outline_color, font=font)
            draw.text((x-1, y+1), text=text, fill=outline_color, font=font)
            draw.text((x+1, y-1), text=text, fill=outline_color, font=font)
            draw.text((x+1, y+1), text=text, fill=outline_color, font=font)
            # Regular Text
            draw.text(xy, text=text, fill=text_color, font=font)

        font = ImageFont.truetype("impact.ttf", 32)
        textwrapped = "\n".join(textwrap.wrap(text, 32))
        draw_with_border(textwrapped, (24, 24), (255, 255, 255), (0, 0, 0))

    def fry(img) -> Image.Image:
        import deeppyer, asyncio
        async def main():
            return await deeppyer.deepfry(img=img, flares=False)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(main())

    text = ""
    if not os.isatty(0): # Data is being piped in use it instead of fortune
        for line in sys.stdin:
            text += line + "\n"
        print(text)

    img = get_cat_img()
    # img = fry(img)
    draw = ImageDraw.Draw(img)
    # text = owo_text(text)
    write_text_on_draw(draw, text)
    # img.show()
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    sys.stdout.buffer.write(img_byte_arr.getvalue())
    img.close()


if __name__ == '__main__':
    build_cat_image()