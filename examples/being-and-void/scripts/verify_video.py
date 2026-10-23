"""Check a delivered MP4 against an exact code-video frame contract."""
import argparse
import json
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("video", type=Path)
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--frames", type=int, required=True)
    a = p.parse_args()
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format",
        "-of", "json", str(a.video)
    ])
    info = json.loads(raw)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    audio = next(s for s in info["streams"] if s["codec_type"] == "audio")
    num, den = map(int, video["r_frame_rate"].split("/"))
    observed_frames = int(video.get("nb_read_frames") or video.get("nb_frames") or 0)
    expected_duration = a.frames / a.fps
    actual_duration = float(info["format"]["duration"])
    checks = {
        "video_codec": video["codec_name"] == "h264",
        "audio_codec": audio["codec_name"] == "aac",
        "dimensions": (video["width"], video["height"]) == (a.width, a.height),
        "fps": num / den == a.fps,
        "frames": observed_frames == a.frames,
        "duration": abs(actual_duration - expected_duration) <= 1 / a.fps,
    }
    result = {
        "video": str(a.video.resolve()), "expected_frames": a.frames,
        "observed_frames": observed_frames, "duration": actual_duration,
        "checks": checks, "passed": all(checks.values())
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
