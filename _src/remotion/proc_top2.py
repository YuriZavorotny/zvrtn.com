import cv2, numpy as np, glob, os
fs = sorted(glob.glob('/home/claude/cover/frg/*.png'))
OUT = '/home/claude/cover/frg_top'; os.makedirs(OUT, exist_ok=True)
X0, X1, Y1 = 960, 1860, 190
ref = cv2.imread(fs[70]); strip = ref[:Y1, X0:X1].copy()
hsv = cv2.cvtColor(strip, cv2.COLOR_BGR2HSV)
red = ((hsv[..., 0] < 8) | (hsv[..., 0] > 165)) & (hsv[..., 1] > 120) & (hsv[..., 2] > 90)
m = np.zeros(red.shape, np.uint8)
for x in range(red.shape[1]):
    ys = np.where(red[:, x])[0]
    if len(ys): m[ys[0]:, x] = 1
m = cv2.dilate(m, np.ones((25, 25), np.uint8))
patch = cv2.inpaint(strip, m, 15, cv2.INPAINT_TELEA)
bl = cv2.GaussianBlur(patch, (0, 0), 14)
mf = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 14)[..., None]
patch = (patch * (1 - mf) + bl * mf).astype(np.uint8)
alpha = np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 9) * 2 - 0.0, 0, 1)[..., None]
for i in range(66, 110):
    im = cv2.imread(fs[i]); roi = im[:Y1, X0:X1].astype(np.float32)
    im[:Y1, X0:X1] = (roi * (1 - alpha) + patch * alpha).astype(np.uint8)
    out = cv2.resize(im[:, 191:191 + 1725], (1440, 900), interpolation=cv2.INTER_AREA)
    cv2.imwrite('%s/%04d.jpg' % (OUT, i - 66), out, [cv2.IMWRITE_JPEG_QUALITY, 93])
cv2.imwrite('/tmp/topstrip.jpg', np.vstack([strip, patch]))
