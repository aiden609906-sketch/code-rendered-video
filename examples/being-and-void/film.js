(() => {
'use strict';
const W=1920,H=1080,FPS=30,DUR=90,PI=Math.PI,TAU=PI*2;
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const ease=v=>{v=clamp(v);return v*v*(3-2*v)};
const lerp=(a,b,t)=>a+(b-a)*t;
const col={paper:'#EEE8DB',ink:'#263C3A',muted:'#6F7770',clay:'#AF5C40',gold:'#AE813E',teal:'#315957'};
function prng(seed){return()=>{seed|=0;seed=seed+0x6D2B79F5|0;let v=Math.imul(seed^seed>>>15,1|seed);v^=v+Math.imul(v^v>>>7,61|v);return((v^v>>>14)>>>0)/4294967296}}
const rand=prng(220026);
const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('world'),antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});
renderer.setSize(W,H,false);renderer.setPixelRatio(1);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.18;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const scene=new THREE.Scene();scene.background=new THREE.Color(col.paper);scene.fog=new THREE.Fog(col.paper,22,48);
const camera=new THREE.PerspectiveCamera(36,W/H,.1,100);
const hemi=new THREE.HemisphereLight(0xfff8e8,0x6d807b,2.0);scene.add(hemi);
const key=new THREE.DirectionalLight(0xffe1ae,4.0);key.position.set(-5,10,7);key.castShadow=true;key.shadow.mapSize.set(1024,1024);Object.assign(key.shadow.camera,{left:-10,right:10,top:10,bottom:-10,near:.1,far:35});key.shadow.bias=-.0003;key.shadow.normalBias=.03;key.shadow.radius=5;scene.add(key);
const fill=new THREE.DirectionalLight(0xb4d4d7,1.4);fill.position.set(5,6,-7);scene.add(fill);
const texCanvas=document.createElement('canvas');texCanvas.width=texCanvas.height=256;const tg=texCanvas.getContext('2d');tg.fillStyle='#909090';tg.fillRect(0,0,256,256);for(let i=0;i<18000;i++){tg.fillStyle=`rgba(255,255,255,${rand()*.22})`;tg.fillRect(rand()*256,rand()*256,1,1)}
const bump=new THREE.CanvasTexture(texCanvas);bump.wrapS=bump.wrapT=THREE.RepeatWrapping;bump.repeat.set(3,2);
const ceramic=new THREE.MeshPhysicalMaterial({color:col.clay,roughness:.40,metalness:.05,clearcoat:.38,clearcoatRoughness:.35,bumpMap:bump,bumpScale:.018});
const cream=new THREE.MeshPhysicalMaterial({color:0xe7ddc7,roughness:.62,bumpMap:bump,bumpScale:.025});
const darkMat=new THREE.MeshStandardMaterial({color:0x274d49,roughness:.55,metalness:.14});
const wood=new THREE.MeshStandardMaterial({color:0x76553a,roughness:.65,bumpMap:bump,bumpScale:.045});
const gold=new THREE.MeshPhysicalMaterial({color:0xcfa25d,roughness:.25,metalness:.75});
const floor=new THREE.Mesh(new THREE.PlaneGeometry(150,150),new THREE.MeshStandardMaterial({color:0xeee8db,roughness:.93}));floor.rotation.x=-PI/2;floor.receiveShadow=true;scene.add(floor);
function mesh(geo,mat,parent,x=0,y=0,z=0){let m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m}
function box(parent,w,h,d,x,y,z,mat=cream){return mesh(new THREE.BoxGeometry(w,h,d),mat,parent,x,y,z)}
function group(){let q=new THREE.Group();scene.add(q);return q}
function pot(parent,x=0,z=0,s=1){let q=new THREE.Group();q.position.set(x,0,z);q.scale.setScalar(s);parent.add(q);let pp=[[0,.02],[.84,.02],[1.0,.12],[1.15,.45],[1.42,1.2],[1.62,2.30],[1.59,2.55],[1.46,2.60],[1.43,2.48],[1.45,2.28],[1.27,1.2],[.94,.45],[0,.35]].map(a=>new THREE.Vector2(...a));let body=mesh(new THREE.LatheGeometry(pp,96),ceramic,q);let rim=mesh(new THREE.TorusGeometry(1.515,.055,12,96),gold,q,0,2.55,0);rim.rotation.x=PI/2;let water=mesh(new THREE.CylinderGeometry(1.31,1.31,.035,96),new THREE.MeshPhysicalMaterial({color:0x638d8b,roughness:.12,metalness:.38,transparent:true,opacity:.86}),q,0,1.65,0);water.visible=false;let plugMat=ceramic.clone();plugMat.transparent=true;let plug=mesh(new THREE.LatheGeometry([[0,.36],[.96,.36],[1.28,1.2],[1.44,2.55],[0,2.55]].map(a=>new THREE.Vector2(...a)),96),plugMat,q);plug.visible=false;return{q,body,rim,water,plug}}
const hook=group(),hpot=pot(hook,1.5,0,1.15);hpot.plug.visible=true;
const relation=group();const halfA=mesh(new THREE.TorusGeometry(2.0,.42,24,96,PI),darkMat,relation,-.3,2.5,0);const halfB=mesh(new THREE.TorusGeometry(2.0,.42,24,96,PI),cream,relation,-.3,2.5,0);halfB.rotation.z=PI;const rods=new THREE.Group();relation.add(rods);const rodA=box(rods,.65,3.3,.65,-1.2,1.65,0,ceramic),rodB=box(rods,.65,1.65,.65,1.2,.825,0,darkMat);
const vessel=group(),vpot=pot(vessel,1.4,0,1.12);const turn=mesh(new THREE.CylinderGeometry(2.25,2.4,.25,96),darkMat,vessel,1.4,.12,0);vpot.q.position.y=.25;
const room=group();const roomFloor=box(room,8,.20,6,0,.1,0,wood);const wallM=new THREE.MeshStandardMaterial({color:0xc6c3af,roughness:.85,bumpMap:bump,bumpScale:.06});
box(room,.22,4,6,-4,2,0,wallM);box(room,.22,4,6,4,2,0,wallM);box(room,8,4,.22,0,2,-3,wallM);
box(room,3,4,.28,-2.5,2,3,wallM);box(room,2,.9,.28,0,3.55,3,wallM);box(room,.7,4,.28,1.35,2,3,wallM);box(room,.5,4,.28,3.75,2,3,wallM);box(room,1.8,1.5,.28,2.6,.75,3,wallM);box(room,1.8,1,.28,2.6,3.5,3,wallM);
const doorPivot=new THREE.Group();doorPivot.name='doorPivot';doorPivot.position.set(-1,0,3.18);room.add(doorPivot);box(doorPivot,2,3.1,.13,1,1.55,0,darkMat);const windowMat=darkMat.clone();windowMat.transparent=true;const shutter=box(room,1.8,1.5,.16,2.6,2.25,3.18,windowMat);shutter.name='shutter';
for(let x of[-1.07,1.07])box(room,.09,3.2,.36,x,1.6,3.08,wood);box(room,2.2,.10,.36,0,3.16,3.08,wood);
for(let x of[1.66,3.54])box(room,.09,1.6,.36,x,2.25,3.08,wood);for(let y of[1.46,3.04])box(room,1.97,.09,.36,2.6,y,3.08,wood);
const sunPatch=mesh(new THREE.PlaneGeometry(2,5.5),new THREE.MeshBasicMaterial({color:0xffd791,transparent:true,opacity:.0,depthWrite:false}),room,0,.22,.0);sunPatch.rotation.x=-PI/2;sunPatch.rotation.z=.1;
const roomTable=mesh(new THREE.CylinderGeometry(1,1,.18,64),wood,room,0,.7,-1.2);box(room,.16,.6,.16,0,.35,-1.2,wood);pot(room,-2,-1.5,.43);
const wheel=group(),wheelBody=new THREE.Group();wheelBody.position.set(0,2.65,0);wheel.add(wheelBody);mesh(new THREE.TorusGeometry(2.3,.13,16,96),wood,wheelBody);mesh(new THREE.TorusGeometry(.50,.18,16,64),wood,wheelBody);const spokes=[];for(let i=0;i<30;i++){let a=i*TAU/30,m=mesh(new THREE.CylinderGeometry(.034,.050,1.60,8),wood,wheelBody,Math.cos(a)*1.45,Math.sin(a)*1.45,0);m.rotation.z=a-PI/2;spokes.push(m)}const axle=mesh(new THREE.CylinderGeometry(.235,.235,4,32),gold,wheel,0,2.65,4);axle.rotation.x=PI/2;
const together=group();const tp=pot(together,-3,0,.64);const miniWheel=wheelBody.clone();miniWheel.position.set(0,1.8,0);miniWheel.scale.setScalar(.64);together.add(miniWheel);const miniRoom=room.clone();miniRoom.scale.setScalar(.30);miniRoom.position.set(3,.0,0);together.add(miniRoom);
const ending=group(),epot=pot(ending,1.7,0,1.03);epot.water.visible=true;
const all=[hook,relation,vessel,room,wheel,together,ending];
const ctx=document.getElementById('type').getContext('2d');
const grain=document.createElement('canvas');grain.width=W;grain.height=H;let gg=grain.getContext('2d');for(let i=0;i<53000;i++){gg.fillStyle=i%2?'#503F28':'#FFFFFF';gg.globalAlpha=.04+rand()*.12;gg.fillRect(rand()*W,rand()*H,.5+rand()*1.4,.5+rand()*1.4)}
function text(s,x,y,size=52,color=col.ink,font='Noto',align='left'){ctx.fillStyle=color;ctx.font=`${size}px ${font}`;ctx.textAlign=align;ctx.textBaseline='middle';ctx.fillText(s,x,y)}
function stroke(points,color,width=2){ctx.beginPath();ctx.moveTo(...points[0]);for(let p of points.slice(1))ctx.lineTo(...p);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap='round';ctx.lineJoin='round';ctx.stroke()}
function mark(s,n,dark=false){text(`0${n}  /  ${s}`,92,75,24,dark?'#BCC7BD':col.muted);stroke([[92,113],[160,113]],dark?'#C49B5B':col.gold,3)}
const cues=[
 [0,3,'一只杯子，最有用的部分是什么？'],[3,6,'是看得见的陶土，还是其中的【空】？'],[6,9,'从这个问题，走近「有无相生」'],
 [9,13,'《道德经》第二章说：【有无相生】'],[13,16.5,'长与短、高与下，也在比较中显现'],[16.5,20,'许多概念，需要相对的一面才能成立'],
 [20,24,'第十一章，又给出三个具体的例子'],[24,28,'陶土塑成器皿，给它边界与形状'],[28,31.5,'中间的空间，才让它能够盛水'],[31.5,35,'器形与中空，一起成就这只器皿'],
 [35,39,'墙壁围成房屋，门窗让空间连通'],[39,43,'门可以通行，窗可以引入光线'],[43,47,'屋内可以居住，也因为留出了空间'],[47,50,'实体与空处，在这里共同起作用'],
 [50,54,'三十根辐条，汇到同一个车毂'],[54,58,'车毂中心的孔，给车轴留下位置'],[58,63,'看得见的结构，配合能够容纳的空间'],
 [63,67,'由此联想：画面有留白，景物更鲜明'],[67,71,'音乐有间歇，节奏才有呼吸'],[71,75,'话语有停顿，意味也能慢慢展开'],
 [75,79,'「无」在这些例子里，是可供使用的空间'],[79,83,'「有」提供形体，「无」让作用展开'],
 [83,86.5,'有之以为利，无之以为用'],[86.5,90,'给事物以形，也给可能留白']
];
function rich(s,x,y,size,color,align='center'){const parts=s.split(/(【[^】]*】)/).filter(Boolean);ctx.font=`${size}px Noto`;let widths=parts.map(s=>ctx.measureText(s.replace(/[【】]/g,'')).width);let total=widths.reduce((a,b)=>a+b,0);let X=align==='center'?x-total/2:x;ctx.textAlign='left';ctx.textBaseline='middle';for(let i=0;i<parts.length;i++){ctx.fillStyle=parts[i].startsWith('【')?col.clay:color;ctx.fillText(parts[i].replace(/[【】]/g,''),X,y);X+=widths[i]}}
function subtitle(t,dark=false){let cue=cues.find(c=>t>=c[0]&&t<c[1]);if(!cue)return;let a=ease((t-cue[0])/.22)*ease((cue[1]-t)/.24);ctx.save();ctx.globalAlpha=a;if((t>=35&&t<50)||(t>=63&&t<67)){ctx.font='51px Noto';let width=ctx.measureText(cue[2].replace(/[【】]/g,'')).width+80;ctx.beginPath();ctx.roundRect(960-width/2,906,width,89,12);ctx.fillStyle=dark?'#173F37C9':'#EEE8DBEB';ctx.fill()}rich(cue[2],960,952,51,dark?'#F4EBD8':col.ink);ctx.restore()}
function source(s,dark=false){text(s,94,1028,21,dark?'#94AAA2':'#878A7F');text('有无相生',1825,1028,23,dark?'#94AAA2':'#878A7F','Ma','right')}
function cameraAt(x,y,z,tx,ty,tz){camera.position.set(x,y,z);camera.lookAt(tx,ty,tz)}
function setup(dark=false){all.forEach(o=>o.visible=false);windowMat.opacity=0;camera.fov=36;camera.updateProjectionMatrix();const bg=dark?'#142E2B':col.paper;scene.background.set(bg);scene.fog.color.set(bg);floor.material.color.set(bg);key.intensity=dark?4.2:4;hemi.intensity=dark?1.1:2;fill.intensity=dark?2:1.4;floor.visible=true}
function hookScene(u){hook.visible=true;hpot.q.rotation.y=u*.12;hpot.plug.material.opacity=1-ease((u-2.5)/2.5);hpot.plug.visible=u<5;cameraAt(7.4-1.1*ease(u/9),6.4+1.3*ease(u/9),10.8,0,1.35,0);mark('器与空',1);text('一只杯子',165,330,112,col.ink,'Ma');text('哪里最有用？',165,475,112,col.ink,'Ma');if(u>4){ctx.globalAlpha=ease((u-4)/1);text('看见形，也看见空。',182,660,38,col.muted);ctx.globalAlpha=1}}
function relationScene(u){relation.visible=true;const p=ease((u-3)/2);halfA.visible=halfB.visible=u<5;halfA.rotation.y=u*.18;halfB.rotation.y=u*.18;rods.visible=u>=4;rods.scale.setScalar(Math.max(.001,p));rodA.scale.y=1;rodB.scale.y=1+.28*Math.sin(u*.7);cameraAt(6*Math.sin(u*.08),5.3,12.6,0,2,0);mark('相待而显',2);text('有',260,340,185,col.ink,'Ma');text('无',1480,340,185,col.clay,'Ma');if(u>=5)text('相生',960,195,94,col.ink,'Ma','center');source('《道德经》第二章 · 本片的一种通俗解读')}
function vesselScene(u){vessel.visible=true;vpot.q.rotation.y=u*.23;vpot.q.scale.set(1.12,lerp(.20,1.12,ease(u/3)),1.12);turn.rotation.y=u*.6;vpot.water.visible=u>=6;vpot.water.scale.setScalar(Math.max(.01,ease((u-6)/2)));vpot.water.position.y=lerp(.5,1.85,ease((u-6)/4));cameraAt(6-2*ease(u/15),7.5+1.0*Math.sin(u*.13),11.4-.9*ease(u/15),.35,1.4,0);mark('埏埴以为器',3);text('有形',175,335,118,col.clay,'Ma');text('可盛',175,470,118,col.ink,'Ma');text('陶土成器 · 中空承水',180,669,35,col.muted);source('《道德经》第十一章 · 器皿意象')}
function roomScene(u){room.visible=true;doorPivot.rotation.y=-1.58*ease((u-1)/4);windowMat.opacity=1-ease((u-2.2)/3);shutter.visible=windowMat.opacity>.001;sunPatch.material.opacity=.32*ease((u-3)/3);let a=ease((u-6)/4),b=ease((u-10)/5);camera.fov=36+14*b;camera.updateProjectionMatrix();cameraAt(8*(1-a),6-2.7*a-.75*b,12-4*a-7.1*b,0,1.35,-1.0);mark('凿户牖以为室',4);source('《道德经》第十一章 · 房屋意象');if(u<7){text('开一扇门',1430,245,75,col.ink,'Ma','center');text('便有一条路',1430,340,75,col.clay,'Ma','center')}}
function wheelScene(u){wheel.visible=true;wheelBody.rotation.z=-u*.28;axle.position.z=lerp(4.8,0,ease((u-4)/5));axle.visible=u>3;cameraAt(6.0-3.7*ease(u/13),5.2,11.5,0,2.4,0);mark('三十辐共一毂',5);text('孔',1510,340,144,col.clay,'Ma','center');text('容轴之处',1510,510,41,col.ink,'Noto','center');source('《道德经》第十一章 · 车轮与车毂示意')}
function mountain(u){ctx.fillStyle=col.paper;ctx.fillRect(0,0,W,H);for(let j=0;j<5;j++){let y=400+j*100,amp=105+j*14;ctx.beginPath();ctx.moveTo(-50,H);for(let x=-50;x<=W+50;x+=8){let xx=x+u*(8+j*3);let z=y-amp*(.5+.25*Math.sin(xx*.004+j*2.3)+.22*Math.sin(xx*.009+j));ctx.lineTo(x,z)}ctx.lineTo(W+50,H);ctx.closePath();ctx.fillStyle=['#CBD0C3','#B4C0B3','#8AA59B','#587F75','#31594F'][j];ctx.globalAlpha=.7;ctx.fill()}ctx.globalAlpha=1;ctx.beginPath();ctx.arc(1440-u*8,300,95,0,TAU);ctx.fillStyle='#E9C99B';ctx.fill()}
function inkScene(u){floor.visible=false;if(u<4){mountain(u);mark('留白的联想',6);text('画外有境',280,240,113,col.ink,'Ma')}else if(u<8){ctx.fillStyle=col.paper;ctx.fillRect(0,0,W,H);mark('留白的联想',6);let q=u-4;for(let i=0;i<36;i++){let x=190+i*43,y=505+42*Math.sin(i*.7+q*.8);let a=(i>13&&i<22)?0:.75;ctx.globalAlpha=a;ctx.beginPath();ctx.arc(x,y,7+(i%4)*2,0,TAU);ctx.fillStyle=col.ink;ctx.fill()}ctx.globalAlpha=1;text('声',400,290,140,col.ink,'Ma');text('息',1290,640,140,col.clay,'Ma');stroke([[805,485],[1125,485]],col.gold,2)}else{ctx.fillStyle=col.paper;ctx.fillRect(0,0,W,H);mark('留白的联想',6);text('间',960,470,370,col.ink,'Ma','center');ctx.globalAlpha=.4;stroke([[620,720],[1300,720]],col.gold,2);ctx.globalAlpha=1}source('当代创作联想 · 非《道德经》逐字原意',u<4)}
function togetherScene(u){together.visible=true;tp.q.rotation.y=u*.2;miniWheel.rotation.z=-u*.20;miniRoom.rotation.y=-.3;miniRoom.getObjectByName('doorPivot').rotation.y=-1.58;miniRoom.getObjectByName('shutter').visible=false;cameraAt(5.5*Math.sin(u*.035),6.6,14.3,0,1.25,0);mark('形与用',7);text('形体',365,235,88,col.clay,'Ma','center');text('空间',1500,235,88,col.ink,'Ma','center');source('《道德经》第十一章 · 有之以为利，无之以为用')}
function endingScene(u){ending.visible=true;epot.q.rotation.y=u*.14;epot.water.position.y=1.7;cameraAt(6,7.5,11.8,.2,1.5,0);mark('有无相生',8,true);text('有无相生',180,340,150,'#F2E8D1','Ma');text('给事物以形',195,555,61,'#D7C9A8','Ma');text('也给可能留白',195,650,61,'#D7C9A8','Ma');source('《道德经》第十一章 · 片尾句为创作表达',true)}
const shots=[{a:0,b:9,f:hookScene},{a:9,b:20,f:relationScene},{a:20,b:35,f:vesselScene},{a:35,b:50,f:roomScene},{a:50,b:63,f:wheelScene},{a:63,b:75,f:inkScene},{a:75,b:83,f:togetherScene},{a:83,b:90,f:endingScene}];
window.DURATION=DUR;
window.FILM_META={cues,shots:shots.map(({a,b})=>({a,b}))};
window.ART={renderer,scene,camera,hemi,key,fill,floor,ceramic,cream,darkMat,wood,gold,wallM,windowMat,doorPivot,shutter,sunPatch,turn,hook,hpot,relation,halfA,halfB,rods,rodA,rodB,vessel,vpot,room,wheel,wheelBody,axle,together,tp,miniRoom,miniWheel,ending,epot,ctx,grain,cues,prng,mesh,box,pot,all};
window.renderFrame=t=>{const f=clamp(Math.floor(t*FPS+1e-6),0,DUR*FPS-1),T=f/FPS,s=shots.find(s=>T>=s.a&&T<s.b),u=T-s.a,dark=T>=83;ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.clearRect(0,0,W,H);setup(dark);s.f(u);renderer.render(scene,camera);ctx.globalAlpha=.32;ctx.drawImage(grain,0,0);ctx.globalAlpha=1;subtitle(T,dark||(T>=63&&T<67))};
})();
