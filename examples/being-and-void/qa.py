"""Seek across scenes, test repeated frames, measure cue widths, and capture cut boundaries."""
import base64, hashlib, io, json, os
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
if (ROOT.parent/'.browsers').is_dir():
    os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH',str(ROOT.parent/'.browsers'))
plan=json.loads((ROOT/'plan.json').read_text(encoding='utf-8'))
out=ROOT/'preview';out.mkdir(exist_ok=True)
with sync_playwright() as pw:
    angle=os.environ.get('CODE_VIDEO_ANGLE','swiftshader')
    browser=pw.chromium.launch(headless=True,args=['--use-angle='+angle,'--enable-webgl','--ignore-gpu-blocklist'])
    page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'index.html').as_uri());page.evaluate('document.fonts.ready')
    page.evaluate('async()=>{for(const f of document.fonts)await document.fonts.load(`52px "${f.family}"`)}')
    cdp=page.context.new_cdp_session(page)
    def capture(t):
        page.evaluate('t=>renderFrame(t)',t)
        return base64.b64decode(cdp.send('Page.captureScreenshot',{'format':'jpeg','quality':95,'fromSurface':True})['data'])
    targets=[4,11,27,41,52,65,77,86]
    tests=[]
    for i,t in enumerate(targets):
        first=capture(t);capture(targets[(i+3)%len(targets)]);again=capture(t)
        equal=hashlib.sha256(first).digest()==hashlib.sha256(again).digest()
        tests.append({'time':t,'cross_scene_seek_deterministic':equal})
    widths=page.evaluate('''()=>{let c=document.createElement('canvas').getContext('2d');c.font='51px Noto';return FILM_META.cues.map(s=>({start:s[0],end:s[1],width:c.measureText(s[2].replace(/[【】]/g,'')).width,text:s[2]}))}''')
    cuts=page.evaluate('FILM_META.cuts || null') or [s['start_frame'] for s in plan['scenes'][1:]]
    frame_numbers=[f for cut in cuts for f in (cut-1,cut)]
    sheet=Image.new('RGB',(1920,300*((len(frame_numbers)+3)//4)),'#242C2C');d=ImageDraw.Draw(sheet)
    for i,f in enumerate(frame_numbers):
        im=Image.open(io.BytesIO(capture(f/30))).convert('RGB');im.thumbnail((480,270))
        x=i%4*480;y=i//4*300;sheet.paste(im,(x,y));d.text((x+8,y+275),f'frame {f} / {f/30:.3f}s',fill='white')
    sheet.save(out/'cut_frames.jpg',quality=93)
    # A full-resolution frame where the camera passes through the doorway.
    (out/'room_close.jpg').write_bytes(capture(48))
    report={'seek_tests':tests,'max_subtitle_width':max(s['width'] for s in widths),'cue_count':len(widths),'errors':errors,'cut_frames':frame_numbers}
    report['passed']=all(s['cross_scene_seek_deterministic'] for s in tests) and max(s['width'] for s in widths)<1740 and not errors
    (out/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    browser.close()
    if not report['passed']:raise SystemExit(1)
