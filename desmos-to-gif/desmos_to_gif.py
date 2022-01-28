from PIL import Image
import re
import base64
import io


def get_images(html_path: str):
    html = open(html_path, 'r').read()
    regex = r"src\=[\"\']data\:image\/png\;base64\,([A-Za-z0-9\+\/]+\=*)[\"\']"
    images = []
    for base64_str in re.findall(regex, html):
        buf = io.BytesIO(base64.b64decode(base64_str))
        img = Image.open(buf)
        images.append(img)
    return images


def save_gif(html_path: str, save_path: str, speed: float = 1.0):
    frames = get_images(html_path)
    if len(frames) == 0:
        raise ValueError("No acceptable image found in the HTML")
    delay = int((4000.0/speed)/len(frames)+0.5)
    save_format = save_path[save_path.rfind('.')+1:].upper()
    frames[0].save(save_path, format=save_format,
                   append_images=frames[1:],
                   save_all=True,
                   duration=delay, loop=0,
                   quality=95, optimize=True)


filepath = input("Enter HTML file path: ").strip()
savepath = input("Enter GIF file path: ").strip()
speed = float(input("Enter playing speed: ").strip())

save_gif(filepath, savepath, speed)
