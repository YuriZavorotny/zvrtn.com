import sys; sys.path.insert(0,'.')
from retitle import *
from PIL import Image, ImageFont, ImageDraw
import numpy as np
O=Image.open('orig/azure-02.jpg').convert('RGB'); A=np.array(O).astype(int)
S=[259,319,378,438,497,556,615,675,735,794,853,912,972,1031,1091,1150,1209,1268,1327]
COLS=[(425,585),(590,800),(802,1012),(1015,1225),(1228,1438),(1440,1650),(1652,1862),(1865,1962)]
def ink(box):
    x0,y0,x1,y1=box; r=A[y0:y1,x0:x1]; d=(765-r.sum(axis=2))>120; ys,xs=np.where(d)
    return xs.min()+x0,xs.max()+x0+1,ys.min()+y0,ys.max()+y0+1
# measurements on row 3 (117604) and row 4
t=438
sx0,sx1,sy0,sy1=ink((425,t+5,585,t+30)); cap1=sy0-t
size=exact(REG,"117604",sx1-sx0)
n0,n1,_,_=ink((590,t+5,800,t+30)); size2=exact(REG,"VM Scale Set Health Metrics",n1-n0)
t4=497
_,_,g0,_=ink((1015,t4+30,1225,t4+50)); _,_,f0,_=ink((1015,t4+5,1225,t4+28)); pitch=g0-f0
SIZE=size2
GRAY=(92,92,92); BLUE=(10,118,205)
print('cap1',cap1,'size',size,size2,'pitch',pitch,GRAY,BLUE)
def put(im,x,cap,text,color):
    f=ImageFont.truetype(REG,int(round(SIZE*S_))); bb=f.getbbox(text); c=f.getbbox("H")
    w=int(bb[2])+8*S_; h=int(bb[3]-c[1])+8*S_
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).text((0,4*S_-c[1]),text,font=f,fill=255)
    m=m.resize((w//S_,h//S_),Image.LANCZOS); im.paste(Image.new('RGB',m.size,color),(x,cap-4),m)
S_=4
# blank template row from row 3
tpl=O.crop((380,S[3],2000,S[4]+1)).copy()
ImageDraw.Draw(tpl).rectangle((414-380,3,1962-380,57),fill=(255,255,255))
def xstart(i): # left x of text in column i, measured from row 3 ink
    return ink((COLS[i][0],t+5,COLS[i][1],t+30))[0]
XS=[xstart(i) for i in range(8)]
def row(im,p,vals):
    y=S[p]; im.paste(tpl,(380,y))
    for i,v in enumerate(vals):
        lines=v if isinstance(v,list) else [v]
        for k,l in enumerate(lines):
            put(im,XS[i],y+cap1+k*pitch,l,BLUE if i==3 else GRAY)
R5=["117606","Dynamic Lead Scoring Drift",["Predictive scoring models","diverge after data refresh..."],["Business Apps: Dynamics","365 Sales Insights"],"Mike Johnson","Storage","New","25 Sep 2020"]
R6=["117607","Automation runbook offset",["Schedule offset by UTC+2","for tenants in Central Europe..."],"Automation: Inventory","Sara Lindgren","ASME","New","24 Sep 2020"]
R7=["117608","Peering latency spikes",["Latency variance between West","and North Europe regions..."],"Networking: Azure Peering Service","Ahmad Khalil","Networking","New","24 Sep 2020"]
R17=["117617","Cognitive Search indexer timeouts",["Indexers fail intermittently on large","datasets..."],"AI & Analytics: Cognitive Search","Tomas Eriksen","Compute","New","13 Sep 2020"]
R18=["117618","Key Vault policy propagation",["Access policy changes take","up to 30 min to apply..."],"Security: Azure Key Vault","Nina Berg","Security","In Review","12 Sep 2020"]
R19=["117619","Monitor alert duplicates",["Autoscale events trigger","duplicate alert emails..."],"Management: Azure Monitor","Omar Haddad","Management","New","11 Sep 2020"]
# --- clean 02 (no hover): rows 5..7 rerendered
c=O.copy()
# test: render row 3 itself into a copy for comparison
test=O.copy(); row(test,3,["117604","VM Scale Set Health Metrics",["Health metrics delayed during","scale-down operations..."],["Compute: Virtual Machine Scale","Sets"],"Helena Petrova","Compute","New","25 Sep 2020"])
Image.fromarray(np.vstack([np.array(O.crop((400,420,2000,520))),np.array(test.crop((400,420,2000,520)))])).save('tcmp.png')
for p,r in [(5,R5),(6,R6),(7,R7)]: row(c,p,r)
for p,v in [(4,'Networking'),(9,'Compute'),(14,'Compute')]:
    ImageDraw.Draw(c).rectangle((1440,S[p]+3,1650,S[p]+56),fill=(255,255,255)); put(c,XS[5],S[p]+cap1,v,GRAY)
ln=O.crop((380,376,2000,381))
for p in range(4,10): c.paste(ln,(380,S[p]-2))
c.save('img/azure-02c.jpg',quality=95)
# filtered: positions
f=Image.new('RGB',O.size); f.paste(c)
src=[0,1,2,3,5,6,8,9,10,11,12,13,14,15]
for p,r in enumerate(src):
    h=S[p+1]-S[p]; f.paste(c.crop((380,S[r],2000,S[r]+h)),(380,S[p]))
row(f,14,R17); row(f,15,R18); row(f,16,R19)
ln=O.crop((380,376,2000,381))
for p in range(1,17): f.paste(ln,(380,S[p]-2))
f.save('img/azure-02f.jpg',quality=95)
