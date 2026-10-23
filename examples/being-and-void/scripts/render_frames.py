"""Render a deterministic HTML scene to six-frame preview or H.264 video.

Example: python scripts/render_frames.py project/index.html --frames 1800 --preview preview.jpg
         python scripts/render_frames.py project/index.html --frames 1800 --output visual.mp4
Use --t0/--speed for a segment of a longer scene. Requires Playwright Chromium and FFmpeg.
"""
import argparse
import base64
import hashlib
import io
import os
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("html", type=Path)
    p.add_argument("--frames", type=int, required=True)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--t0", type=float, default=0.0)
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--angle", choices=["swiftshader", "d3d11"], default="swiftshader", help="Use verified hardware rendering on Windows, or portable SwiftShader")
    p.add_argument("--executable", type=Path, help="Chromium/Chrome/Edge binary; default is automatic discovery")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preview", type=Path, help="Six-frame contact-sheet JPEG")
    mode.add_argument("--output", type=Path, help="H.264 MP4 output")
    a = p.parse_args()
    if min(a.frames, a.fps, a.width, a.height) <= 0 or a.speed <= 0:
        p.error("frames, fps, dimensions and speed must be positive")
    if not a.html.is_file():
        p.error(f"HTML file missing: {a.html}")

    if "PLAYWRIGHT_BROWSERS_PATH" not in os.environ:
        local_browsers = Path.cwd() / ".browsers"
        if local_browsers.is_dir() and any(local_browsers.glob("chromium-*")):
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(local_browsers.resolve())

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        opts = {
            "headless": True,
            "args": ["--use-angle=" + a.angle, "--enable-webgl", "--ignore-gpu-blocklist",
                     "--disable-background-timer-throttling", "--hide-scrollbars"],
        }
        executable = a.executable
        if executable is None and not Path(pw.chromium.executable_path).is_file() and os.name == "nt":
            local = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
            candidates = [
                local / "Google" / "Chrome" / "Application" / "chrome.exe",
                Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Google" / "Chrome" / "Application" / "chrome.exe",
                Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
                Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
            ]
            executable = next((candidate for candidate in candidates if candidate.is_file()), None)
        if executable:
            if not executable.is_file():
                p.error(f"Browser executable missing: {executable}")
            opts["executable_path"] = str(executable.resolve())
            print(f"Browser: {executable}", flush=True)
        else:
            print(f"Browser: {pw.chromium.executable_path}", flush=True)
        browser = pw.chromium.launch(**opts)
        try:
            context = browser.new_context(viewport={"width": a.width, "height": a.height}, device_scale_factor=1)
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(a.html.resolve().as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            page.evaluate("""async () => {
              for (const f of [...document.fonts]) await document.fonts.load(`${f.weight} 32px "${f.family}"`);
            }""")
            if page.evaluate("typeof window.renderFrame") != "function":
                raise RuntimeError("HTML must expose window.renderFrame(t)")
            duration = page.evaluate("Number(window.DURATION)")
            last_t = a.t0 + (a.frames - 1) / a.fps * a.speed
            if not (duration > last_t):
                raise RuntimeError(f"Scene DURATION {duration} is shorter than last sample at {last_t:.6f}s")
            cdp = context.new_cdp_session(page)
            cdp.send("Page.enable")

            def shot(i):
                t = a.t0 + i / a.fps * a.speed
                page.evaluate("t => window.renderFrame(t)", t)
                if errors:
                    raise RuntimeError("Scene error: " + errors[-1])
                data = cdp.send("Page.captureScreenshot", {
                    "format": "jpeg", "quality": 95, "fromSurface": True,
                    "captureBeyondViewport": False,
                })["data"]
                return base64.b64decode(data)

            if a.preview:
                from PIL import Image, ImageDraw
                indices = sorted({round((a.frames - 1) * j / 5) for j in range(6)})
                thumbs = []
                for i in indices:
                    im = Image.open(io.BytesIO(shot(i))).convert("RGB")
                    im.thumbnail((480, 270))
                    thumbs.append((i, im))
                h = max(im.height for _, im in thumbs) + 26
                sheet = Image.new("RGB", (480 * 3, h * 2), "#111319")
                d = ImageDraw.Draw(sheet)
                for j, (i, im) in enumerate(thumbs):
                    x, y = (j % 3) * 480, (j // 3) * h
                    sheet.paste(im, (x, y))
                    d.text((x + 6, y + h - 21), f"frame {i}, t={a.t0 + i/a.fps*a.speed:.3f}s", fill="white")
                a.preview.parent.mkdir(parents=True, exist_ok=True)
                sheet.save(a.preview, quality=92)
                repeat = hashlib.sha256(shot(indices[0])).digest() == hashlib.sha256(shot(indices[0])).digest()
                print(f"Preview: {a.preview}; deterministic repeat={repeat}")
                if not repeat:
                    raise RuntimeError("Repeated capture differed at the same timestamp")
            else:
                a.output.parent.mkdir(parents=True, exist_ok=True)
                cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
                       "-f", "image2pipe", "-framerate", str(a.fps), "-vcodec", "mjpeg",
                       "-i", "pipe:0", "-an", "-c:v", "libx264", "-preset", "medium",
                       "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(a.output)]
                proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    for i in range(a.frames):
                        proc.stdin.write(shot(i))
                        if i % (a.fps * 5) == 0:
                            print(f"rendered {i}/{a.frames}", flush=True)
                    proc.stdin.close()
                    error = proc.stderr.read().decode("utf-8", "replace")
                    if proc.wait() != 0:
                        raise RuntimeError(error)
                except Exception:
                    proc.kill()
                    raise
                print(f"Rendered {a.frames} frames -> {a.output}")
            context.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main()
