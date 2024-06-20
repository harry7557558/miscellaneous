import re
from hashlib import md5
import os
import markdown
from datetime import datetime
import json

image_dir = 'attachments/'

image_files = [file for file in os.listdir(image_dir)
               if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
image_files.sort(key=lambda x: -int(x.split('-')[0]))


def snowflake_time(snowflake):
    return datetime.utcfromtimestamp(((int(snowflake) >> 22) + 1420070400000) / 1000)

html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Discord Image Viewer</title>
    <link rel="stylesheet" href="https://spirulae.github.io/gallery/style.css" />
    <script src="https://spirulae.github.io/gallery/script.js"></script>
</head>
<body>
    <div id="display-container" style="display:none">
        <img id="display" src="" />
    </div>

    <div id="content">
"""

prev_month = None

for fi in range(len(image_files)):
    filename = image_files[fi]

    snowflake = filename.split('-')[0]
    date = snowflake_time(snowflake)
    month = date.strftime('%B %Y')
    date = date.strftime('%Y-%m-%d')

    if month != prev_month:
        if prev_month != None:
            html += "<br/><hr/>\n"
        html += "<h1>" + month + "</h1>\n"
        prev_month = month
    html += f"""<a href="{filename}"><img id="{snowflake}" src="{filename}" title="{date}" loading="lazy"/></a>\n"""

html += """
    </div>
</body>"""


open("attachments/index.html", "w").write(html)
