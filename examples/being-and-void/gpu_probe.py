"""Verify native GPU rendering and benchmark the exact capture path before a long render."""
import base64,hashlib,json,os,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
if (ROOT.parent/'.browsers').is_dir():os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH',str(ROOT.parent/'.browsers'))
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--use-angle=d3d11','--enable-webgl','--ignore-gpu-blocklist'])
    page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((ROOT/'index.html').as_uri());page.evaluate('document.fonts.ready');page.evaluate('async()=>{await document.fonts.load("96px Ma");await document.fonts.load("43px Noto")}')
    info=page.evaluate('''()=>{let gl=ART.renderer.getContext(),e=gl.getExtension('WEBGL_debug_renderer_info');return {vendor:e?gl.getParameter(e.UNMASKED_VENDOR_WEBGL):'',renderer:e?gl.getParameter(e.UNMASKED_RENDERER_WEBGL):'',version:gl.getParameter(gl.VERSION)}}''')
    session=page.context.new_cdp_session(page)
    def shot(t):
        page.evaluate('t=>renderFrame(t)',t)
        return base64.b64decode(session.send('Page.captureScreenshot',{'format':'jpeg','quality':95,'fromSurface':True})['data'])
    a=shot(4);shot(41);bframe=shot(4)
    info['deterministic']=hashlib.sha256(a).digest()==hashlib.sha256(bframe).digest()
    (ROOT/'preview'/'gpu_cup.jpg').write_bytes(a);(ROOT/'preview'/'gpu_room.jpg').write_bytes(shot(41))
    start=time.perf_counter()
    for i in range(30):shot(35+i/30)
    info['capture_fps']=30/(time.perf_counter()-start);info['errors']=errors
    (ROOT/'preview'/'gpu_probe.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
    print(json.dumps(info,indent=2));b.close()
    if not info['deterministic'] or errors:raise SystemExit(1)
