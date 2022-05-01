#!/usr/bin/env python
import io, sys, subprocess, os, argparse
import textwrap, re, random

from PIL import Image, ImageDraw, ImageFont
import requests

def build_cat_image():
    arg_parser = argparse.ArgumentParser(description='Caption an AI generated cat image with stdin and stdout the image')
    
    # Add all necessary cli args
    arg_parser.add_argument("-o", "--owo_text", help="Makes text from stdin cuter :3", action=argparse.BooleanOptionalAction)
    arg_parser.add_argument("-f", "--deep_fry", help="Deep fry the auto-generated cat", action=argparse.BooleanOptionalAction)

    args = arg_parser.parse_args()

    def get_cat_img() -> Image.Image:
        # Get an image of a cat from public internet cat generating robo slave
        # To add offline mode, might add capabilities to grab from local files instead
        url = 'https://thiscatdoesnotexist.com/'
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content))

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

    def write_text_on_draw(draw: ImageDraw.ImageDraw, text: str, bottom: bool):
        xy = (24, 24)
        font_size = 32
        wrap_length = 32
        if bottom:
            # TODO: Adjust text anchors to draw from bottom instead of taking an x, y approach,
            # As well as enabling properly centered text: https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
            xy = (24, 400)
            font_size = 64
            wrap_length = 16

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

        font = ImageFont.truetype("impact.ttf", font_size)
        textwrapped = "\n".join(textwrap.wrap(text, wrap_length))
        draw_with_border(textwrapped, xy, (255, 255, 255), (0, 0, 0))

    def fry(img) -> Image.Image:
        import deeppyer, asyncio
        async def main():
            return await deeppyer.deepfry(img=img, flares=False)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(main())

    text = ""
    bottom_text = ""
    if not os.isatty(0): # Data is being piped in use it instead of fortune
        for line in sys.stdin:
            text += line + "\n"
        print(text)
        split_text = text.split("|")
        if len(split_text) > 1:
            text = split_text[0]
            bottom_text = split_text[-1]

    img = get_cat_img()
    if args.deep_fry:
        img = fry(img)
    draw = ImageDraw.Draw(img)
    if args.owo_text:
        text = owo_text(text)
    write_text_on_draw(draw, text, False)
    write_text_on_draw(draw, bottom_text, True)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    sys.stdout.buffer.write(img_byte_arr.getvalue())
    img.close()

if __name__ == '__main__':
    build_cat_image()