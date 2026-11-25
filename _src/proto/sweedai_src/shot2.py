import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':2000,'height':1248})
        boxes={}
        for s in '0123':
            await pg.goto(f'file://"+__import__("os").path.abspath("ab.html")+"?s={s}');await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'../img/sweedai-0{s}.jpg',type='jpeg',quality=95)
            for i in ['gen','add','start']:
                el=await pg.query_selector('#'+i)
                if el: boxes[s+i]=await el.bounding_box()
        print(json.dumps(boxes))
        await b.close()
asyncio.run(main())
