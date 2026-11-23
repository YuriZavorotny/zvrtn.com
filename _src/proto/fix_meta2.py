import sys; sys.path.insert(0,'.')
from retitle import *
from PIL import Image
import numpy as np
def edit(im,box,orig,new,font,align='l'):
    a=np.array(im).astype(int); x0,y0,x1,y1=box
    reg=a[y0:y1,x0:x1]
    edge=np.concatenate([reg[0],reg[-1],reg[:,0],reg[:,-1]]); bg=tuple(int(v) for v in np.median(edge,axis=0))
    diff=np.abs(reg-np.array(bg)).sum(axis=2)>90
    ys,xs=np.where(diff); ix0,ix1,iy0,iy1=xs.min()+x0,xs.max()+x0+1,ys.min()+y0,ys.max()+y0+1
    col=textcolor(a,box)
    size=exact(font,orig,ix1-ix0)
    f=ImageFont.truetype(font,100)
    isz=round(size/100*100*S)/S  # keep float size
    # render at fractional size via integer size*S scaling
    sz=size
    im.paste(Image.new('RGB',(x1-x0,y1-y0),bg),(x0,y0))
    fnt=ImageFont.truetype(font,int(round(sz*S)))
    w=fnt.getlength(new)/S
    x=ix0 if align=='l' else int(round(ix1-w))
    # captop of orig = ink top (first char cap/ascender)
    if len(col)==3 and font==REG and 'Feedback' in new: col=(0,120,212)
    if font==SB and 'Feedback' in new: col=(0,120,212)
    render_f(im,new,font,sz,x,iy0,col)
    return x
def render_f(im,text,font,size,x,captop,color):
    f=ImageFont.truetype(font,int(round(size*S))); bb=f.getbbox(text); cap=f.getbbox("H")
    w=int(bb[2])+8*S; h=int(bb[3]-cap[1])+8*S
    c=Image.new('L',(w,h),0); ImageDraw.Draw(c).text((0,4*S-cap[1]),text,font=f,fill=255)
    m=c.resize((w//S,h//S),Image.LANCZOS)
    im.paste(Image.new('RGB',m.size,color),(x,captop-4),m)
SBf,RGf=SB,REG

src=Image.open('orig/azure-01.jpg').convert('RGB')
# --- 04
im=Image.open('orig/azure-04.jpg').convert('RGB')
edit(im,(186,122,560,146),"AI - Compute  /  AI - Compute  /  Machine Learning Service","Compute  /  Virtual Machines",SBf)
edit(im,(850,122,900,146),"New","Escalated",SBf)
edit(im,(994,122,1100,146),"Not defined","Service Improvement",SBf)
nx=edit(im,(1256,120,1390,148),"Constantin Eggert","Juan Mart\u00ednez",SBf,'r')
av=src.crop((1812,492,1832,512)).resize((25,25),Image.LANCZOS)
im.paste(Image.new('RGB',(40,30),(255,255,255)),(1224,119)); im.paste(av,(nx-34,121))
edit(im,(1230,508,1368,526),"Smiths Business","Telefonica Global Services",SBf,'r')
edit(im,(1226,527,1368,550),"by Jon Dobrzeniecki","by Juan Mart\u00ednez",RGf,'r')
edit(im,(1226,563,1368,588),"OneList Feedback","Partner Center Feedback",RGf,'r')
im.save('img/azure-04.jpg',quality=95)
# --- 03
im=Image.open('orig/azure-03.jpg').convert('RGB')
edit(im,(818,474,1300,498),"AI - Compute  -  AI - Compute  -  Machine Learning Service","Compute  -  Virtual Machines",SBf)
edit(im,(818,908,1100,932),"Smiths Business","Telefonica Global Services",SBf)
edit(im,(818,962,1100,986),"OneList Feedback","Partner Center Feedback",SBf)
edit(im,(818,1016,1100,1040),"Jon Dobrzenicki","Juan Mart\u00ednez",SBf)
edit(im,(818,800,1100,824),"7 Jan 2019","7 Jan 2020",SBf)
im.save('img/azure-03.jpg',quality=95)
# --- 05
im=Image.open('orig/azure-05.jpg').convert('RGB')
edit(im,(362,800,600,824),"OneList Feedback","Partner Center Feedback",SBf)
edit(im,(704,800,960,824),"Jon Dobrzeniecki","Juan Mart\u00ednez",SBf)
im.save('img/azure-05.jpg',quality=95)
