const {chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const name=process.argv[2],dir='fr_'+name;const cfg=JSON.parse(fs.readFileSync(name+'.json'));
 fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
 const W=2000,H=1248,FPS=30;
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:W,height:H}});
 await p.goto(`http://localhost:8765/player3.html?cfg=${name}.json`);await p.waitForFunction('window.ready');await p.waitForTimeout(500);
 // таймлайн
 const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
 let cx=W*.62,cy=H*.8;const F=[];// кадры: {x,y,click?}
 const hold=(s)=>{for(let i=0;i<Math.round(s*FPS);i++)F.push({x:cx,y:cy})};
 hold(1.5);
 for(const st of cfg.steps){ if(st[0]!='click')continue;
  const bb=await (await p.$('#'+st[1])).boundingBox();
  const tx=bb.x+Math.min(bb.width/2,222),ty=bb.y+bb.height/2,x0=cx,y0=cy,n=Math.round(.7*FPS);
  for(let i=1;i<=n;i++){const k=ease(i/n);F.push({x:x0+(tx-x0)*k,y:y0+(ty-y0)*k})}
  cx=tx;cy=ty;hold(.15);F.push({x:cx,y:cy,click:st[1]});hold(1.5);
 }
 hold(.8);
 {const n=Math.round(.6*FPS);for(let i=1;i<=n;i++){const t=i/n;F.push({x:cx,y:cy,nda:t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2})}}
 for(let i=0;i<Math.round(1.8*FPS);i++)F.push({x:cx,y:cy,nda:1});
 let rp=null;
 for(let i=0;i<F.length;i++){const f=F[i];
  await p.mouse.move(f.x,f.y);
  if(f.click){await p.evaluate(id=>document.getElementById(id).click(),f.click);rp={x:f.x,y:f.y,i}}
  const pr=rp?(i-rp.i)/(.5*FPS):-1;await p.evaluate(([x,y,q])=>setRipple(x,y,q),[rp?rp.x:0,rp?rp.y:0,pr]);
  await p.evaluate(v=>setNda(v),f.nda||0);
  await p.screenshot({path:`${dir}/${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});
 }
 console.log(name,'frames',F.length);await b.close();
})();
