"""Portable build: python build.py [--preview-only | --finish-only]."""
import argparse, json, os, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'plan.json').read_text(encoding='utf-8'))
env=os.environ.copy();env['PYTHONUTF8']='1'
if (ROOT.parent/'.browsers').is_dir():env.setdefault('PLAYWRIGHT_BROWSERS_PATH',str(ROOT.parent/'.browsers'))
def run(args):subprocess.run([str(s) for s in args],cwd=ROOT,env=env,check=True)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    mode=ap.add_mutually_exclusive_group();mode.add_argument('--preview-only',action='store_true');mode.add_argument('--finish-only',action='store_true')
    ap.add_argument('--angle',choices=['swiftshader','d3d11'],default='swiftshader')
    a=ap.parse_args();out=ROOT/'output';out.mkdir(exist_ok=True)
    env['CODE_VIDEO_ANGLE']=a.angle
    if a.preview_only:
        for s in P['scenes']:
            run([sys.executable,'scripts/render_frames.py','index.html','--angle',a.angle,'--frames',s['frames'],'--fps',30,'--t0',s['start_frame']/30,'--preview','preview/'+s['id']+'.jpg'])
        run([sys.executable,'qa.py']);return
    if not a.finish_only:
        run([sys.executable,'score.py']);run([sys.executable,'qa.py'])
        run([sys.executable,'scripts/render_frames.py','index.html','--angle',a.angle,'--frames',2700,'--fps',30,'--output','output/visual.mp4'])
    final=out/'being_and_void_90s.mp4'
    run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',out/'visual.mp4','-i',out/'score.wav',
         '-map','0:v:0','-map','1:a:0','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p',
         '-af','loudnorm=I=-18:TP=-2:LRA=8,aresample=48000,atrim=0:90,asetpts=PTS-STARTPTS',
         '-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709',
         '-c:a','aac','-b:a','192k','-ar','48000','-t','90','-movflags','+faststart',final])
    result=subprocess.run([sys.executable,str(ROOT/'scripts/verify_video.py'),str(final),'--width','1920','--height','1080','--fps','30','--frames','2700'],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',check=True)
    (out/'verification.json').write_text(result.stdout,encoding='utf-8');print(result.stdout)
    run([sys.executable,'scripts/contact_sheet.py',final,'preview/delivery_2s.jpg','--interval','2'])
    run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-ss','84.5','-i',final,'-frames:v','1','preview/poster.jpg'])
if __name__=='__main__':main()
