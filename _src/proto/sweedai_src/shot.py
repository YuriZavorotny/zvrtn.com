import asyncio,json
from playwright.async_api import async_playwright
K=2000/1440
async def main():
    out='../sweedai_remotion/public'; import os; os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1440,'height':899},device_scale_factor=K)
        R={}
        for s in ['0','e','f','g','2','1','3']:
            await pg.goto(f'file://'+__import__('os').path.abspath('ab.html')+'?s={s}');await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{out}/s{s}.png',clip={'x':0,'y':0,'width':1440,'height':899})
            boxes=await pg.evaluate('''()=>{const K=2000/1440,r=e=>{const b=e.getBoundingClientRect();return [b.x*K,b.y*K,b.width*K,b.height*K].map(Math.round)};const o={};
              for(const id of ['gen','genbtn','add','start','ta','dh','BB','P']){const e=document.getElementById(id);if(e)o[id]=r(e)}
              o.dc=[...document.querySelectorAll('.dc')].map(r);o.aic=[...document.querySelectorAll('.aic')].map(r);o.tr=[...document.querySelectorAll('.tb .tr')].map(r);
              const ta=document.getElementById('ta');if(ta){const cs=getComputedStyle(ta);o.taPad=[parseFloat(cs.paddingLeft)*K,parseFloat(cs.paddingTop)*K]}
              return o}''')
            R[s]=boxes
        json.dump(R,open(f'{out}/boxes.json','w'),indent=0)
        print(json.dumps({k:{kk:v for kk,v in R[k].items() if kk in('gen','genbtn','add','start','ta','dc','BB','taPad')} for k in R}))
        await b.close()
asyncio.run(main())
