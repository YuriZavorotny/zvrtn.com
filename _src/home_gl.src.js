(function(){
"use strict";
var small=innerWidth<760;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}

/* ---------- разметка проектов ---------- */
var ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="square" stroke-linejoin="miter"><path d="M2.5 12h17M13 5.5l6.5 6.5-6.5 6.5"/></svg>';
document.getElementById("list").innerHTML=PROJECTS.map(function(p,i){
  var src=(small&&p.video480)?p.video480:p.video;
  return '<article class="row item '+(i%2?'l':'r')+'" style="--y:'+(620*i)+'"'+(p.tint?' data-tint="'+p.tint.join(",")+'"':'')+'>'+
    '<div class="asset"><video src="'+esc(src)+'" poster="'+esc(src.replace(/\.mp4$/,".jpg"))+'" muted loop playsinline preload="'+(i<2?'auto':'metadata')+'" autoplay></video></div>'+
    '<a class="txt" href="'+esc(p.href)+'">'+
      '<h3 class="ttl"><span class="arr" aria-hidden="true">'+ARROW+'</span><span class="nm">'+esc(p.title)+'</span></h3>'+
      '<div class="meta"><p class="role">'+esc(p.role)+'</p><p class="dt">'+esc(p.period)+'</p>'+(p.metric||[]).map(function(m){return '<p class="mt">'+esc(m)+'</p>'}).join('')+'</div>'+
    '</a>'+
  '</article>';
}).join("");

var items=[].slice.call(document.querySelectorAll(".item")).map(function(li){
  return {li:li,hoverEls:[li.querySelector(".asset"),li.querySelector(".txt")],asset:li.querySelector(".asset"),video:li.querySelector("video"),
          hover:0,hoverTween:null,tex:null,ok:false,visible:false,
          tint:(li.dataset.tint||"1,1,1").split(",").map(Number)};
});

/* автоплей только на экране */
if("IntersectionObserver" in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    var it=items.filter(function(i){return i.asset===e.target})[0]; if(!it) return;
    it.visible=e.isIntersecting;
    if(e.isIntersecting){if(it.video.preload!=="auto")it.video.preload="auto";var pr=it.video.play();pr&&pr.catch&&pr.catch(function(){})} else it.video.pause();
  })},{rootMargin:"200px"});
  items.forEach(function(it){io.observe(it.asset)});
}

/* автоплей: добиваем, если браузер отложил */
function kick(){items.forEach(function(it){if(it.visible!==false&&it.video.paused){var p=it.video.play();p&&p.catch&&p.catch(function(){})}})}
items.forEach(function(it){it.video.addEventListener("canplay",kick)});
["pointerdown","touchstart","keydown","scroll","visibilitychange"].forEach(function(ev){addEventListener(ev,kick,{passive:true})});
setTimeout(kick,600);setTimeout(kick,2000);
/* сторож: если видео на экране застряло без данных, перезапускаем загрузку */
setInterval(function(){items.forEach(function(it){var v=it.video;
  if(it.visible===false||v.readyState>=2){it.stuck=0;return}
  if(v.readyState===it.lastRS&&v.buffered.length===it.lastBuf)it.stuck=(it.stuck||0)+1;else it.stuck=0;
  it.lastRS=v.readyState;it.lastBuf=v.buffered.length;
  if(it.stuck>=2){it.stuck=0;v.preload="auto";v.load();var p=v.play();p&&p.catch&&p.catch(function(){})}
})},2000);
/* ---------- WebGL ---------- */
var canvas=document.getElementById("gl");
var reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
var gl=null;
try{ gl=canvas.getContext("webgl2",{alpha:false,antialias:false,premultipliedAlpha:true}) }catch(e){}
var touch=matchMedia("(hover: none), (pointer: coarse)").matches||innerWidth<760;
if(!gl||reduce){ return }                       // без WebGL остаются обычные видео

var extCBF=gl.getExtension("EXT_color_buffer_float")||gl.getExtension("EXT_color_buffer_half_float");
gl.getExtension("OES_texture_float_linear");
var haveFluid=!!extCBF;

function sh(type,src){
  var s=gl.createShader(type); gl.shaderSource(s,src); gl.compileShader(s);
  if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)+"\n"+src.slice(0,200));
  return s;
}
function prog(vs,fs){
  var p=gl.createProgram(); gl.attachShader(p,sh(gl.VERTEX_SHADER,vs)); gl.attachShader(p,sh(gl.FRAGMENT_SHADER,fs));
  gl.linkProgram(p); if(!gl.getProgramParameter(p,gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
  var u={},n=gl.getProgramParameter(p,gl.ACTIVE_UNIFORMS);
  for(var i=0;i<n;i++){var a=gl.getActiveUniform(p,i);u[a.name]=gl.getUniformLocation(p,a.name)}
  return {p:p,u:u};
}

/* ---------- 1. жидкость: свечение за курсором ---------- */
var FS_VS="#version 300 es\nin vec2 aPos;out vec2 vUv;void main(){vUv=aPos*.5+.5;gl_Position=vec4(aPos,0.,1.);}";
var HEAD="#version 300 es\nprecision highp float;in vec2 vUv;out vec4 o;\n";

var P_SPLAT=prog(FS_VS,HEAD+"uniform sampler2D uTarget;uniform float aspectRatio;uniform vec3 uColor;uniform vec2 uPointer;uniform float uRadius;\n"+
 "void main(){vec2 p=vUv-uPointer;p.x*=aspectRatio;vec3 splat=exp(-dot(p,p)/uRadius)*uColor;o=vec4(texture(uTarget,vUv).xyz+splat,1.);}");

/* для красителя: берём максимум вместо суммы, чтобы пятно не росло при кружении */
var P_SPLATMAX=prog(FS_VS,HEAD+"uniform sampler2D uTarget;uniform float aspectRatio;uniform vec3 uColor;uniform vec2 uPointer;uniform float uRadius;\n"+
 "void main(){vec2 p=vUv-uPointer;p.x*=aspectRatio;vec3 splat=exp(-dot(p,p)/uRadius)*uColor;o=vec4(max(texture(uTarget,vUv).xyz,splat),1.);}");

var P_ADVECT=prog(FS_VS,HEAD+"uniform sampler2D uVelocity;uniform sampler2D uSource;uniform float dt;uniform float diss;uniform float aspectRatio;\n"+
 "void main(){vec2 v=texture(uVelocity,vUv).xy;vec2 c=vUv-dt*vec2(v.x/aspectRatio,v.y);"+
 "vec4 r=texture(uSource,c);o=r/(1.+diss*dt);}");

var P_DISPLAY=prog(FS_VS,HEAD+"uniform sampler2D uDye;uniform vec3 uBg;uniform float uSeed,uTime,uAmt;\n"+
 "float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}\n"+
 "vec3 pal(float t){return .5+.5*cos(6.28318*(t+vec3(0.,.33,.67)));}\n"+
 "float D(vec2 uv){vec2 o=vec2(.005,.005);return (texture(uDye,uv+o).r+texture(uDye,uv-o).r+texture(uDye,uv+vec2(o.x,-o.y)).r+texture(uDye,uv+vec2(-o.x,o.y)).r)*.25;}\n"+
 "void main(){\n"+
 " vec2 e=vec2(.008,0.);\n"+
 " vec2 g=vec2(D(vUv+e.xy)-D(vUv-e.xy),D(vUv+e.yx)-D(vUv-e.yx));\n"+
 " vec2 off=normalize(g+1e-6)*.007*clamp(length(g)*14.,0.,1.);\n"+
 " float i=D(vUv);\n"+
 " vec3 a=smoothstep(0.,.5,vec3(D(vUv+off),i,D(vUv-off)));\n"+
 " float ph=i*1.3+vUv.x*.45-vUv.y*.25+uTime*.00002;\n"+
 " vec3 tint=.3+.7*pal(ph);\n"+
 " vec3 col=uBg-a*(uBg-tint)*.24*uAmt;\n"+
 " col+=(h(gl_FragCoord.xy+uSeed)-.5)/255.;o=vec4(col,1.);}");

var quad=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,quad);
gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);   // один большой треугольник
function bindFS(p){var l=gl.getAttribLocation(p.p,"aPos");gl.bindBuffer(gl.ARRAY_BUFFER,quad);gl.enableVertexAttribArray(l);gl.vertexAttribPointer(l,2,gl.FLOAT,false,0,0)}

function makeFBO(w,h){
  var t=gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D,t);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA16F,w,h,0,gl.RGBA,gl.HALF_FLOAT,null);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  var f=gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER,f);
  gl.framebufferTexture2D(gl.FRAMEBUFFER,gl.COLOR_ATTACHMENT0,gl.TEXTURE_2D,t,0);
  gl.viewport(0,0,w,h); gl.clearColor(0,0,0,1); gl.clear(gl.COLOR_BUFFER_BIT);
  return {t:t,f:f,w:w,h:h};
}
function makeDouble(w,h){var a=makeFBO(w,h),b=makeFBO(w,h);return{r:a,w:b,swap:function(){var t=this.r;this.r=this.w;this.w=t}}}

var W=0,H=0,dpr=1,aspect=1,vel=null,dye=null;
function initFluid(){
  if(!haveFluid) return;
  aspect=W/H;
  var dw=Math.round(Math.min(320,200*Math.max(1,aspect))), dh=Math.round(dw/aspect);
  var vw=Math.round(128*Math.max(1,aspect)), vh=Math.round(vw/aspect);
  dye=makeDouble(dw,dh); vel=makeDouble(vw,vh);
}
function blit(target){
  if(target){gl.bindFramebuffer(gl.FRAMEBUFFER,target.f);gl.viewport(0,0,target.w,target.h)}
  else{gl.bindFramebuffer(gl.FRAMEBUFFER,null);gl.viewport(0,0,canvas.width,canvas.height)}
  gl.drawArrays(gl.TRIANGLES,0,3);
}
function tex(unit,t){gl.activeTexture(gl.TEXTURE0+unit);gl.bindTexture(gl.TEXTURE_2D,t)}

function splat(db,x,y,r,g,b,radius,useMax){
  var P=useMax?P_SPLATMAX:P_SPLAT;
  gl.useProgram(P.p);bindFS(P);
  tex(0,db.r.t);gl.uniform1i(P.u.uTarget,0);
  gl.uniform1f(P.u.aspectRatio,aspect);gl.uniform2f(P.u.uPointer,x,y);
  gl.uniform3f(P.u.uColor,r,g,b);gl.uniform1f(P.u.uRadius,radius);
  blit(db.w);db.swap();
}
function advect(db,dt,diss){
  gl.useProgram(P_ADVECT.p);bindFS(P_ADVECT);
  tex(0,vel.r.t);gl.uniform1i(P_ADVECT.u.uVelocity,0);
  tex(1,db.r.t);gl.uniform1i(P_ADVECT.u.uSource,1);
  gl.uniform1f(P_ADVECT.u.dt,dt);gl.uniform1f(P_ADVECT.u.diss,diss);gl.uniform1f(P_ADVECT.u.aspectRatio,aspect);
  blit(db.w);db.swap();
}

/* указатель */
var ptr={x:.5,y:.5,px:0,py:0,moved:false,has:false,dx:0,dy:0};
function onMove(x,y){
  var nx=x/innerWidth, ny=1-y/innerHeight;
  if(ptr.has){ptr.dx+=(x-ptr.px)/innerHeight;ptr.dy+=-(y-ptr.py)/innerHeight}
  ptr.x=nx;ptr.y=ny;ptr.px=x;ptr.py=y;ptr.has=true;ptr.moved=true;
}
addEventListener("pointermove",function(e){onMove(e.clientX,e.clientY)},{passive:true});
addEventListener("touchmove",function(e){var t=e.touches[0];t&&onMove(t.clientX,t.clientY)},{passive:true});

/* ---------- 2. видео-плитки: искажения по краям экрана + волна при наведении ---------- */
var GRID=28;
var VS_Q="#version 300 es\nprecision highp float;\n"+
"in vec2 aUv;out vec2 vUv;\n"+
"uniform vec4 uRect;uniform vec2 uRes;\n"+
"uniform float uViewportTop,uViewportBottom,uEdgeZone,uFisheye,uVelocity,uTime,uHover;\n"+
"void main(){vUv=aUv;vec2 p=aUv-.5;\n"+
" float vpY=mix(uViewportBottom,uViewportTop,aUv.y);\n"+
" float d=abs(vpY-.5)*2.;\n"+
" float enter=smoothstep(1.-uEdgeZone,1.,d);float exit_=1.-smoothstep(1.,1.+uEdgeZone,d);\n"+
" float edge=enter*exit_;\n"+
" float r2=dot(p,p)*4.;\n"+
" p+=p*uFisheye*edge*r2*uVelocity;\n float tt=uTime*.0004;\n float rim=.3+.7*smoothstep(.2,.5,max(abs(p.x),abs(p.y)));\n float amp=.011*sin(uHover*3.14159)*rim;\n p+=vec2(sin(aUv.y*5.+tt*1.3+aUv.x*2.3),cos(aUv.x*4.+tt))*amp;\n"+
" vec2 c=uRect.xy+uRect.zw*.5;\n"+
" vec2 s=c+vec2(p.x,-p.y)*uRect.zw;\n"+
" gl_Position=vec4(s.x/uRes.x*2.-1.,1.-s.y/uRes.y*2.,0.,1.);}";

var FS_Q=HEAD+
"uniform sampler2D uTexture;uniform float uOpacity,uTime,uEdgeZone,uGridSize,uGridStrength,uLensStrength,uCaStrength,uSmearStrength,uLiquidStrength,uLiquidSpeed;\n"+
"uniform float uHover,uRippleStrength,uRippleFrequency,uRippleChroma,uRippleMaxRadius,uRippleFrontSharpness,uRippleBrightness;\n"+
"uniform float uViewportTop,uViewportBottom,uImageAspect,uContainerAspect,uBorderRadius;uniform vec2 uSize;uniform vec3 uTint;\n"+
"float rbox(vec2 p,vec2 hs,float r){vec2 q=abs(p)-hs+r;return min(max(q.x,q.y),0.)+length(max(q,0.))-r;}\n"+
"vec2 cellNoise(vec2 c){return vec2(fract(sin(dot(c,vec2(127.1,311.7)))*43758.5453),fract(sin(dot(c,vec2(269.5,183.3)))*43758.5453))-.5;}\n"+
"vec2 coverUV(vec2 uv){if(uImageAspect>uContainerAspect){float s=uContainerAspect/uImageAspect;uv.x=uv.x*s+(1.-s)*.5;}else{float s=uImageAspect/uContainerAspect;uv.y=uv.y*s+(1.-s)*.5;}return uv;}\n"+
"void main(){\n"+
" float vpY=mix(uViewportBottom,uViewportTop,vUv.y);\n"+
" float dist=abs(vpY-.5)*2.;\n"+
" float effect=smoothstep(1.-uEdgeZone,1.,dist);\n"+
" float dir=vpY>.5?-1.:1.;\n"+
" vec2 cell=floor(vUv*uGridSize)/uGridSize;vec2 noise=cellNoise(cell);\n"+
" float e2=effect*effect;\n"+
" vec2 gridOffset=noise*e2*uGridStrength;\n"+
" vec2 lensDir=vec2(0.,dir);float lensing=e2*uLensStrength;\n"+
" float smear=effect*e2*uSmearStrength*-dir;\n"+
" float waveX=sin(vUv.y*25.+uTime*uLiquidSpeed)*e2*uLiquidStrength;\n"+
" float waveY=cos(vUv.x*18.+uTime*uLiquidSpeed*.7)*e2*uLiquidStrength*.6;\n"+
" vec2 luv=vUv+lensDir*lensing+gridOffset+vec2(waveX,smear+waveY);\n"+
" vec2 rc=luv-.5;float rr=length(rc)*1.4142;\n"+
" float front=uHover*uRippleMaxRadius;float rd=rr-front;\n"+
" float band=exp(-rd*rd*uRippleFrontSharpness);float env=sin(uHover*3.14159);\n"+
" float corner=1.-smoothstep(.65,.95,rr);\n"+
" vec2 rdir=rc/(rr+.0001);\n"+
" float wave=sin((rr-front)*uRippleFrequency);\n"+
" luv+=rdir*band*env*uRippleStrength*wave*corner;\n"+
" float ca=e2*uCaStrength;float rca=band*env*uRippleChroma*corner;\n"+
" vec2 caDir=vec2(0.,dir)*ca+rdir*rca;\n"+
" float r=texture(uTexture,coverUV(luv+caDir)).r;\n"+
" float g=texture(uTexture,coverUV(luv)).g;\n"+
" float b=texture(uTexture,coverUV(luv-caDir)).b;\n"+
" vec3 col=vec3(r,g,b);\n"+
" col+=col*(band*env*uRippleBrightness*corner);\n col*=uTint;\n"+
" vec2 px=vUv*uSize;float d=rbox(px-uSize*.5,uSize*.5,uBorderRadius);\n"+
" float mask=1.-smoothstep(-.5,.5,d);\n"+
" float a=uOpacity*mask;o=vec4(col*a,a);}";

var P_Q=prog(VS_Q,FS_Q);
/* сетка вершин плитки (для искажения «рыбий глаз») */
var gridVerts=[],gridIdx=[];
for(var gy=0;gy<=GRID;gy++)for(var gx=0;gx<=GRID;gx++)gridVerts.push(gx/GRID,gy/GRID);
for(var gy=0;gy<GRID;gy++)for(var gx=0;gx<GRID;gx++){var a=gy*(GRID+1)+gx,b=a+1,c=a+GRID+1,d=c+1;gridIdx.push(a,b,c,b,d,c)}
var vao=gl.createVertexArray();gl.bindVertexArray(vao);
var gb=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,gb);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(gridVerts),gl.STATIC_DRAW);
var aUv=gl.getAttribLocation(P_Q.p,"aUv");gl.enableVertexAttribArray(aUv);gl.vertexAttribPointer(aUv,2,gl.FLOAT,false,0,0);
var ib=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ib);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,new Uint16Array(gridIdx),gl.STATIC_DRAW);
gl.bindVertexArray(null);

var CFG={EDGE_ZONE:.3,GRID_SIZE:20,GRID_STRENGTH:0,LENS_STRENGTH:.3,CA_STRENGTH:.05,SMEAR_STRENGTH:.25,
  LIQUID_STRENGTH:.05,LIQUID_SPEED:.0005,FISHEYE:.3,
  RIPPLE_MAX_RADIUS:1.4,RIPPLE_FRONT_SHARPNESS:10,RIPPLE_STRENGTH:.045,RIPPLE_FREQUENCY:12,RIPPLE_CHROMA:.02,RIPPLE_BRIGHTNESS:.45};

/* телефон: canvas лежит в документе и едет вместе со страницей (нативный скролл), поэтому видео не дрожит относительно текста */
var PAD=touch?320:0;
if(touch){canvas.style.position="absolute";canvas.style.top="0";canvas.style.left="0";canvas.style.willChange="transform"}
items.forEach(function(it){
  it.tex=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,it.tex);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,1,1,0,gl.RGBA,gl.UNSIGNED_BYTE,new Uint8Array([0,0,0,0]));
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  it.failed=false;
  /* волна при наведении: вход .9с, выход .6с */
  function tween(to,dur){
    var from=it.hover,t0=performance.now();cancelAnimationFrame(it.hoverTween);
    (function step(now){var k=Math.min(1,(now-t0)/(dur*1000)),e=1-Math.pow(1-k,3);it.hover=from+(to-from)*e;if(k<1)it.hoverTween=requestAnimationFrame(step)})(t0);
  }
  var hovT=null;
  it.hoverEls.forEach(function(el){
    el.addEventListener("pointerenter",function(){clearTimeout(hovT);it.li.classList.add("hov");tween(1,1.8)});
    el.addEventListener("pointerleave",function(){clearTimeout(hovT);hovT=setTimeout(function(){it.li.classList.remove("hov")},60);tween(0,1.2)});
  });
});

function uploadVideo(it){
  var v=it.video; if(v.readyState<2||it.failed) return false;
  try{
    gl.bindTexture(gl.TEXTURE_2D,it.tex);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,true);
    gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,v);
    if(!it.ok){it.ok=true;it.li.classList.add("gl-on")}
    return true;
  }catch(e){
    it.failed=true; it.ok=false;     // например file://: браузер запрещает текстуры из локальных видео
    it.li.classList.remove("gl-on");
    if(!window.__warned){window.__warned=true;console.warn("Видео не загрузилось в WebGL (откройте страницу через http://, а не file://). Показываю обычное видео.",e)}
    return false;
  }
}
/* ---------- 3. цикл ---------- */
function resize(){
  dpr=Math.min(devicePixelRatio||1,2);W=innerWidth;H=innerHeight;
  canvas.width=Math.round(W*dpr);canvas.height=Math.round((H+PAD*2)*dpr);
  if(touch){canvas.style.width=W+"px";canvas.style.height=(H+PAD*2)+"px"}
  initFluid();
}
resize();addEventListener("resize",function(){resize()});

var last=performance.now(),lastScroll=scrollY,sv=0,idle=0;
var BG=[1,1,1];
var heroEl=document.querySelector(".hero");

function frame(now){
  var OFF=0;
  if(touch){var ty=Math.min(scrollY-PAD,document.documentElement.scrollHeight-(H+PAD*2));OFF=scrollY-ty;canvas.style.transform="translate3d(0,"+ty+"px,0)"}
  var rdt=Math.max(.008,(now-last)/1000)||.016;
  var dt=Math.min(.033,(now-last)/1000)||.016;last=now;

  /* скорость прокрутки в px/с, не зависит от частоты кадров (сглаженная, быстро растёт, медленно гаснет) */
  var dy=Math.abs(scrollY-lastScroll);lastScroll=scrollY;
  var raw=Math.min(1.2,dy/rdt/1500);
  sv+=(raw-sv)*(raw>sv?.05:.04);

  /* фон: жидкость */
  /* разводы живут только на экране «обо мне» */
  var hr=heroEl.getBoundingClientRect(),heroF=Math.max(0,Math.min(1,hr.bottom/(H*.5)));
  if(!touch&&haveFluid&&heroF>0){
    if(ptr.moved&&ptr.py<hr.bottom){
      var sp=Math.hypot(ptr.dx,ptr.dy);
      var amt=Math.min(.30,.10+sp*6);              // потолок яркости: пятно не накапливается
      splat(vel,ptr.x,ptr.y,ptr.dx*25,ptr.dy*25,0,.012);
      splat(dye,ptr.x,ptr.y,amt,amt,amt,.0042,true);
    }
    ptr.dx=ptr.dy=0;ptr.moved=false;
    advect(vel,dt*.5,3.5);
    advect(dye,dt*.5,2.2);
    gl.useProgram(P_DISPLAY.p);bindFS(P_DISPLAY);
    tex(0,dye.r.t);gl.uniform1i(P_DISPLAY.u.uDye,0);
    gl.uniform3f(P_DISPLAY.u.uBg,BG[0],BG[1],BG[2]);gl.uniform1f(P_DISPLAY.u.uSeed,now%97);gl.uniform1f(P_DISPLAY.u.uTime,now);gl.uniform1f(P_DISPLAY.u.uAmt,heroF);
    blit(null);
  }else{
    ptr.dx=ptr.dy=0;ptr.moved=false;
    gl.bindFramebuffer(gl.FRAMEBUFFER,null);gl.viewport(0,0,canvas.width,canvas.height);
    gl.clearColor(BG[0],BG[1],BG[2],1);gl.clear(gl.COLOR_BUFFER_BIT);
  }

  /* плитки */
  gl.bindFramebuffer(gl.FRAMEBUFFER,null);gl.viewport(0,0,canvas.width,canvas.height);
  gl.enable(gl.BLEND);gl.blendFunc(gl.ONE,gl.ONE_MINUS_SRC_ALPHA);
  gl.useProgram(P_Q.p);gl.bindVertexArray(vao);
  var U=P_Q.u;
  gl.uniform2f(U.uRes,W,H+PAD*2);
  gl.uniform1f(U.uTime,now);
  gl.uniform1f(U.uEdgeZone,CFG.EDGE_ZONE);gl.uniform1f(U.uFisheye,CFG.FISHEYE*3);gl.uniform1f(U.uVelocity,sv);
  gl.uniform1f(U.uGridSize,CFG.GRID_SIZE);gl.uniform1f(U.uGridStrength,CFG.GRID_STRENGTH);
  gl.uniform1f(U.uLensStrength,CFG.LENS_STRENGTH);gl.uniform1f(U.uCaStrength,CFG.CA_STRENGTH);
  gl.uniform1f(U.uSmearStrength,CFG.SMEAR_STRENGTH);gl.uniform1f(U.uLiquidStrength,CFG.LIQUID_STRENGTH);gl.uniform1f(U.uLiquidSpeed,CFG.LIQUID_SPEED);
  gl.uniform1f(U.uRippleStrength,CFG.RIPPLE_STRENGTH);gl.uniform1f(U.uRippleFrequency,CFG.RIPPLE_FREQUENCY);
  gl.uniform1f(U.uRippleChroma,CFG.RIPPLE_CHROMA);gl.uniform1f(U.uRippleMaxRadius,CFG.RIPPLE_MAX_RADIUS);
  gl.uniform1f(U.uRippleFrontSharpness,CFG.RIPPLE_FRONT_SHARPNESS);gl.uniform1f(U.uRippleBrightness,CFG.RIPPLE_BRIGHTNESS);
  gl.uniform1f(U.uOpacity,1);gl.uniform1i(U.uTexture,0);

  items.forEach(function(it){
    var r=it.asset.getBoundingClientRect();
    if(r.bottom<-H*.2||r.top>H*1.2){return}
    if(!uploadVideo(it)&&!it.ok) return;
    var vw=it.video.videoWidth||16,vh=it.video.videoHeight||10;
    gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,it.tex);
    gl.uniform4f(U.uRect,r.left,r.top+OFF,r.width,r.height);
    gl.uniform1f(U.uViewportTop,1-r.top/H);gl.uniform1f(U.uViewportBottom,1-r.bottom/H);
    gl.uniform2f(U.uSize,r.width,r.height);
    gl.uniform1f(U.uBorderRadius,0);
    gl.uniform1f(U.uImageAspect,vw/vh);gl.uniform1f(U.uContainerAspect,r.width/r.height);
    gl.uniform1f(U.uHover,it.hover);gl.uniform3f(U.uTint,it.tint[0],it.tint[1],it.tint[2]);
    gl.drawElements(gl.TRIANGLES,gridIdx.length,gl.UNSIGNED_SHORT,0);
  });
  gl.bindVertexArray(null);gl.disable(gl.BLEND);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
})();
