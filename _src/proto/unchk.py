import sys; sys.path.insert(0,'.')
from fix_meta2 import edit, REG, SB  # noqa (fix_meta2 runs its edits again on bak2 -> idempotent)
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
def boxes(im):
    a=np.array(im).astype(int)[670:790,55:110]; m=(a[:,:,2]>170)&(a[:,:,0]<90)
    lab,n=ndimage.label(m); out=[]
    for sl in ndimage.find_objects(lab):
        y,x=sl; out.append((x.start+55,y.start+670,x.stop+55,y.stop+670))
    return out
def uncheck(im):
    for (x0,y0,x1,y1) in [(65,684,82,701),(79,725,96,742),(79,767,96,784)]:
        w=x1-x0; K=4
        ImageDraw.Draw(im).rectangle((x0-1,y0-1,x1,y1),fill=(243,242,240))
        t=Image.new('RGBA',(w*K,w*K),(0,0,0,0)); d=ImageDraw.Draw(t)
        d.rounded_rectangle((0,0,w*K-1,w*K-1),radius=2*K,fill=(50,49,48,255))
        b=int(1.4*K); d.rounded_rectangle((b,b,w*K-1-b,w*K-1-b),radius=K,fill=(255,255,255,255))
        t=t.resize((w,w),Image.LANCZOS); im.paste(t,(x0,y0),t)
for n in ['02f','01','01h']:
    p=f'img/azure-{n}.jpg'; src='orig/azure-01.jpg' if n=='01' else p
    if n=='01h':
        import os
        if not os.path.exists('orig/azure-01h.jpg'): Image.open(p).save('orig/azure-01h.jpg',quality=97)
        src='orig/azure-01h.jpg'
    im=Image.open(src).convert('RGB'); uncheck(im)
    if n!='02f': edit(im,(1880,214,1975,240),"1-50 of 328","1-50 of 240",REG,'r')
    im.save(p,quality=95)
