from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys
import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts')+'/'
REG=D+'Selawik-Regular.ttf'; SB=D+'Selawik-Semibold.ttf'
S=4
def exact(font,text,width):
    f=ImageFont.truetype(font,100); return 100*width/f.getlength(text)
def render(im,text,font,size,x,captop,color):
    f=ImageFont.truetype(font,size*S); bb=f.getbbox(text); cap=f.getbbox("H")
    w=int(bb[2])+8*S; h=int(bb[3]-cap[1])+8*S
    c=Image.new('L',(w,h),0); ImageDraw.Draw(c).text((0,4*S-cap[1]),text,font=f,fill=255)
    m=c.resize((w//S,h//S),Image.LANCZOS)
    layer=Image.new('RGB',m.size,color); im.paste(layer,(x,captop-4),m)
def wrap(text,font,size,width):
    f=ImageFont.truetype(font,size*S); words=text.split(' '); lines=[];cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if f.getlength(t)/S<=width: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def textcolor(a,box):
    x0,y0,x1,y1=box; r=a[y0:y1,x0:x1].reshape(-1,3); s=r.sum(axis=1); d=r[s<np.percentile(s,3)+1]; return tuple(int(v) for v in np.median(d,axis=0))
