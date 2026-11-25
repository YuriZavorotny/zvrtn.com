"""Reel frames for the cover:
A (0..65): mom shot gets our mobile UI on the phone screen; crop x from 96.
B (66..109): mockup shot, cropped further right (x from 191) so the sheet sits off the edge less.
Output 1440x900 jpgs into frg_v6/."""
import cv2, numpy as np, glob, os
fs = sorted(glob.glob('/home/claude/cover/frg/*.png'))
OUT = '/home/claude/cover/frg_v10'; os.makedirs(OUT, exist_ok=True)
SPL = sorted(glob.glob('/home/claude/remo/out/splash5/*.png')); k_spl = 0
t0 = 17.6; log = []

def fill_holes(m):
    h, w = m.shape
    ff = m.copy(); mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(ff, mask, (0, 0), 1)  # outside -> 1
    holes = (ff == 0).astype(np.uint8)
    return m | holes

for i, f in enumerate(fs[:110]):
    t = t0 + i / 25
    im = cv2.imread(f); H, W = im.shape[:2]
    if 18.9 < t and i < 66:
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        m = (((hsv[..., 0] < 6) | (hsv[..., 0] > 168)) & (hsv[..., 1] > 150) & (hsv[..., 2] > 150)).astype(np.uint8)
        m[:, :W // 2] = 0
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        n, lab, st, cen = cv2.connectedComponentsWithStats(m)
        if n > 1:
            j = 1 + np.argmax(st[1:, 4]); x, y, w, h, a = st[j]
            if a > 6000 and 1.5 < h / w < 2.8:
                comp = (lab[y:y + h, x:x + w] == j).astype(np.uint8)
                pad = np.pad(comp, 1)
                filled = fill_holes(pad)[1:-1, 1:-1]
                holes = filled - comp
                holes[int(h * 0.12):] = holes[int(h * 0.12):]  # keep
                holes[:int(h * 0.12)] = 0  # leave the camera notch dark
                comp = comp | holes
                comp = cv2.erode(comp, np.ones((3, 3), np.uint8))
                alpha = cv2.GaussianBlur(comp.astype(np.float32), (3, 3), 0)[..., None]
                ui = cv2.imread(SPL[min(k_spl, len(SPL) - 1)]); k_spl += 1
                src = cv2.resize(ui, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32)
                roi = im[y:y + h, x:x + w].astype(np.float32)
                # keep a touch of the original lighting so it sits in the shot
                lum = cv2.cvtColor(roi.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)[..., None]
                shade = 1.0
                im[y:y + h, x:x + w] = (roi * (1 - alpha) + np.clip(src * shade, 0, 255) * alpha).astype(np.uint8)
                log.append(round(t, 2))
    ox = 96 if i < 66 else 191
    out = cv2.resize(im[:, ox:ox + 1725], (1440, 900), interpolation=cv2.INTER_AREA)
    cv2.imwrite('%s/%04d.jpg' % (OUT, i), out, [cv2.IMWRITE_JPEG_QUALITY, 93])
print('ui frames', len(log), log[:1], log[-1:])
