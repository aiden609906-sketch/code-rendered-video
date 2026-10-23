"""Make a timestamp-labeled 1 fps contact sheet from a rendered MP4."""
import argparse
import io
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("video", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--interval", type=float, default=1.0)
    p.add_argument("--columns", type=int, default=6)
    p.add_argument("--thumb-width", type=int, default=320)
    a = p.parse_args()
    if a.interval <= 0 or a.columns <= 0 or a.thumb_width <= 0:
        p.error("interval, columns and thumb-width must be positive")
    meta = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(a.video)
    ]))
    duration = float(meta["format"]["duration"])
    times = [i * a.interval for i in range(math.ceil(duration / a.interval))]
    thumbs = []
    for t in times:
        data = subprocess.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", str(a.video),
            "-frames:v", "1", "-f", "image2pipe", "-vcodec", "mjpeg", "pipe:1"
        ])
        im = Image.open(io.BytesIO(data)).convert("RGB")
        im.thumbnail((a.thumb_width, a.thumb_width))
        thumbs.append((t, im))
    h = max(im.height for _, im in thumbs) + 28
    rows = math.ceil(len(thumbs) / a.columns)
    sheet = Image.new("RGB", (a.columns * a.thumb_width, rows * h), "#111319")
    draw = ImageDraw.Draw(sheet)
    for i, (t, im) in enumerate(thumbs):
        x, y = (i % a.columns) * a.thumb_width, (i // a.columns) * h
        sheet.paste(im, (x, y))
        draw.text((x + 5, y + h - 22), f"{t:.2f}s", fill="white")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.output, quality=90)
    print(f"{len(thumbs)} frames -> {a.output}")


if __name__ == "__main__":
    main()
