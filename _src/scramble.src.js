/* ====================================================================
   Набор текста «как на печатной машинке / в игровом автомате» (по мотивам Signal-A), для меню и подвала:
   - view:  при появлении в экране буквы по очереди крутятся случайными символами и встают на место
   - resc:  при наведении весь текст на 0.4с перемешивается и собирается слева направо
   ==================================================================== */
(function(){
"use strict";
if(matchMedia("(prefers-reduced-motion: reduce)").matches) return;
var CH="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:',.<>/?`~";
function rnd(){return CH.charAt(Math.floor(Math.random()*CH.length))}

function wrap(el){
  el.innerHTML=el._html;
  var spans=[];
  (function walk(n){
    [].slice.call(n.childNodes).forEach(function(c){
      if(c.nodeType===3){
        var f=document.createDocumentFragment();
        c.textContent.split(/([ \t\r\n]+)/).forEach(function(t){
          if(!t) return;
          if(/^[ \t\r\n]+$/.test(t)){f.appendChild(document.createTextNode(t));return}
          var w=document.createElement("span");w.className="scr-w";w.setAttribute("aria-hidden","true");
          t.split("").forEach(function(ch){var s=document.createElement("span");s.className="scr-c";s.dataset.c=ch;s.textContent=ch;w.appendChild(s);spans.push(s)});
          f.appendChild(w);
        });
        n.replaceChild(f,c);
      }else if(c.nodeType===1) walk(c);
    });
  })(el);
  /* фиксируем ширину букв, чтобы строки не прыгали, пока символы меняются */
  var ws=spans.map(function(s){return s.getBoundingClientRect().width});
  spans.forEach(function(s,i){s.style.width=ws[i]+"px"});
  return spans;
}
function stop(el){ if(el._raf){cancelAnimationFrame(el._raf);el._raf=null;el.innerHTML=el._html} }

function run(el,mode,delay){
  stop(el);
  if(el._html==null) el._html=el.innerHTML;
  el.setAttribute("aria-label",el.textContent);
  var spans=wrap(el),n=spans.length,t0=performance.now()+(delay||0),last=spans.map(function(){return -1e9});
  el.classList.remove("scr-pre");
  function tick(now){
    var t=now-t0,done=true;
    spans.forEach(function(s,i){
      var c=s.dataset.c;
      if(t<0){ s.textContent=(mode==="view"?(i===0?c:""):c); done=false; return }
      if(mode==="view"){
        if(i===0){s.textContent=c;return}
        var d=n>1?i/(n-1)*400:0,lt=t-d;
        if(lt<0){s.textContent="";done=false}
        else if(lt<400){done=false;if(now-last[i]>=19){last[i]=now;s.textContent=rnd()}}
        else s.textContent=c;
      }else{
        var end=200+(n>1?i/(n-1)*200:0);
        if(t<end){done=false;if(now-last[i]>=20){last[i]=now;s.textContent=rnd()}}
        else s.textContent=c;
      }
    });
    if(done){el.innerHTML=el._html;el._raf=null;return}
    el._raf=requestAnimationFrame(tick);
  }
  el._raf=requestAnimationFrame(tick);
}

/* что набираем: только меню */
var list=[];
function add(el,delay){ if(!el) return; el._html=el.innerHTML; el.dataset.d=delay||0; list.push(el) }
[].forEach.call(document.querySelectorAll(".top nav a, .foot span, .foot a, .meta .mt, .recs .rl, [data-scr]"),function(a,i){add(a,(i%4)*70)});
list.forEach(function(el){el.classList.add("scr-pre")});

var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(!e.isIntersecting) return;
  io.unobserve(e.target);
  run(e.target,"view",+e.target.dataset.d||0);
})},{threshold:.1});
list.forEach(function(el){io.observe(el)});

/* наведение на пункт меню */
[].forEach.call(document.querySelectorAll(".top a, .foot a"),function(a){
  a.addEventListener("pointerenter",function(){ if(!a.classList.contains("scr-pre")) run(a,"resc",0) });
});
})();
