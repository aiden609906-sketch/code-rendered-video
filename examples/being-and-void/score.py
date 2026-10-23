"""90-second original score: synthesized plucks, air, clay taps and frame-drum accents."""
import json
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

ROOT=Path(__file__).resolve().parent
PLAN=json.loads((ROOT/'plan.json').read_text(encoding='utf-8'))
SR=48000; N=PLAN['total_frames']*SR//PLAN['fps']
rng=np.random.default_rng(220022)
dry=np.zeros(N,np.float32)

def add(sec,w,level=1):
    a=int(round(sec*SR));b=min(N,a+len(w))
    if b>a:dry[a:b]+=w[:b-a]*level

def pluck(freq,dur=3.5,amp=.1):
    t=np.arange(int(dur*SR),dtype=np.float32)/SR
    signal=np.zeros(len(t),np.float32)
    for h in range(1,11):
        decay=np.exp(-t*(.8+h*.24))
        signal+=np.sin(2*np.pi*freq*h*t+.015*h*h)*decay/(h**1.55)
    attack=1-np.exp(-t*250)
    release=np.minimum(1,(dur-t)/.3)
    signal*=attack*np.maximum(0,release)
    signal+=rng.normal(0,1,len(t)).astype(np.float32)*np.exp(-t*170)*.08
    return signal*amp

def pad(freq,dur,amp=.018):
    t=np.arange(int(dur*SR),dtype=np.float32)/SR
    env=np.minimum(1,t/1.3)*np.minimum(1,(dur-t)/1.8)
    w=np.sin(2*np.pi*freq*t)+.3*np.sin(2*np.pi*freq*2*t)
    return w*np.maximum(0,env)*amp

def tap(sec,freq=410,amp=.04):
    t=np.arange(int(.5*SR),dtype=np.float32)/SR
    w=(np.sin(2*np.pi*freq*t)+.4*np.sin(2*np.pi*freq*2.71*t))*np.exp(-t*15)
    add(sec,w,amp)

def drum(sec,amp=.07):
    t=np.arange(int(.9*SR),dtype=np.float32)/SR
    f=51+28*np.exp(-t*13)
    w=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
    add(sec,w,amp)

# Pentatonic motif, with spaces deliberately left between phrases.
scale=[146.83,174.61,196,220,261.63,293.66,349.23]
phrases=[(0,[0,3,4,2]),(9,[3,4,2,0]),(20,[0,2,3,5]),(35,[4,3,2,0]),(50,[0,2,3,4]),(75,[0,3,4,5]),(83,[4,3,2,0])]
for start,notes in phrases:
    for j,n in enumerate(notes):add(start+j*1.5,pluck(scale[n],4.5,.11))
    for j,n in enumerate(notes[::-1]):
        if start+6+j*1.0<89:add(start+6+j*1.0,pluck(scale[n]*.5,3.7,.055))

for start,end,root in [(0,9,73.415),(9,20,98),(20,35,73.415),(35,50,87.305),(50,63,98),(75,83,73.415),(83,90,73.415)]:
    add(start,pad(root,end-start,.022))
    add(start,pad(root*3,end-start,.012))

for seg in PLAN['scenes'][1:]:
    sec=seg['start_frame']/30
    drum(sec,.065)
    tap(sec,620,.020)
for sec in np.arange(50,62,.5):tap(float(sec),290,.012)
for sec in (24,28,31.5,39,43,54,58,79):tap(sec,520,.025)

# A quiet air movement when the room opens; a filtered water gesture when the vessel fills.
for start,dur,low,high,gain in [(38,3.5,180,1100,.014),(27,2.2,650,3000,.023)]:
    noise=rng.normal(0,1,int(dur*SR)).astype(np.float32)
    filtered=sosfilt(butter(2,[low,high],btype='bandpass',fs=SR,output='sos'),noise)
    env=np.sin(np.linspace(0,np.pi,len(noise)))**2
    add(start,filtered*env,gain)

# Illustrated rests at 63–75 s, including a short, intentional silence at 69 s.
for sec,f in [(63,293.66),(65,220),(67,174.61),(70,220),(72,146.83)]:
    add(sec,pluck(f,2.1,.085))
for f in (146.83,220,293.66):add(86,pad(f,4,.024))

# Deterministic stereo room reflections.
left=dry.copy();right=dry.copy()
for delay,gain in [(.071,.19),(.149,.12),(.281,.08),(.433,.045)]:
    n=int(delay*SR);left[n:]+=dry[:-n]*gain
for delay,gain in [(.089,.18),(.177,.13),(.319,.075),(.487,.04)]:
    n=int(delay*SR);right[n:]+=dry[:-n]*gain
audio=np.stack((left,right),axis=1)
fade=np.minimum(1,np.arange(N)/(SR*.2))*np.minimum(1,(N-np.arange(N))/(SR*1.4))
audio*=np.maximum(0,fade[:,None])
audio=np.tanh(audio*1.2)
audio*=.74/max(np.max(np.abs(audio)),1e-9)
out=ROOT/'output'/'score.wav';out.parent.mkdir(exist_ok=True)
wavfile.write(out,SR,(audio*32767).astype(np.int16))
print(json.dumps({'seconds':N/SR,'samples':N,'peak':float(np.max(np.abs(audio))),'rms':float(np.sqrt(np.mean(audio**2)))},indent=2))
