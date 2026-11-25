import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Video } from "@remotion/media";
import { Opener } from "./Opener";
import { Desktop, DesktopState, L } from "./ui/Desktop";
import { Mobile } from "./ui/Mobile";
import { Cursor, Ripple } from "./ui/Parts";
import { fontCss } from "./theme";

export const FPS = 30;
const OP = 3.4; // opener length (reveal overlaps the reel)
const REVEAL = 2.7;
const A_LEN = 0; // reel shots removed, opener reveals the mockup directly
const B_LEN = 3.08;
const TB = REVEAL + A_LEN; // mockup shot start
const EXP_AT = TB + 3.45;
const EXP = 1.15;
const D0 = EXP_AT + EXP;
const DESK = 15.6;
export const COVER_SECONDS = D0 + DESK;

const S = 1440 / 1725;
const RED = { x0: (1003 - 191) * S, x1: (1806 - 191) * S, y0: 45 * S };
const DS = 1440 / 1210;
const DOX = -78;
const DH = 900 / DS;

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const inOut = Easing.bezier(0.65, 0, 0.35, 1);
const ease = Easing.bezier(0.16, 1, 0.3, 1);

/** The mockup shot: video shrinks into a card, the UI sheet covers the phone graphic, then expands to desktop */
const MockupScene: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const z = 0;
  const v = 1;
  const ox = 0;
  const oy = 0;
  const m = 18;
  const px = ox + RED.x0 * v - m;
  const pw = (RED.x1 - RED.x0) * v + 2 * m;
  const py = oy + 72;
  const ph = 900 - py + 80;
  const e = interpolate(t, [EXP_AT - TB, EXP_AT - TB + EXP], [0, 1], { ...clamp, easing: inOut });
  const x = interpolate(e, [0, 1], [px, 0]);
  const y = interpolate(e, [0, 1], [py, 0]);
  const w = interpolate(e, [0, 1], [pw, 1440]);
  const h = interpolate(e, [0, 1], [ph, 900]);
  const r = interpolate(e, [0, 1], [64, 0]);
  const mScale = w / 412;
  const scroll = interpolate(t, [1.2, 2.1], [0, 300], { ...clamp, easing: inOut }) - interpolate(t, [2.2, 2.75], [0, 300], { ...clamp, easing: inOut });
  const open = spring({ frame: f - 2.95 * fps, fps, config: { damping: 200 } });
  const tapQ = (t - 2.85) / 0.45;
  const dScale = interpolate(e, [0, 1], [pw / 1210, DS]);
  const mobO = interpolate(e, [0.05, 0.3], [1, 0], clamp);
  const deskO = interpolate(e, [0.1, 0.4], [0, 1], clamp);
  const cardO = 1;
  const dState: DesktopState = { set: 1, open: 1, reveal: 3, modal: 0, chip: 0, loading: null, typing: 0, msg: 1, shimmer: 0 };
  return (
    <AbsoluteFill style={{ background: "#f3f4f8" }}>
      <div style={{ position: "absolute", left: ox, top: oy, width: 1440, height: 900, transformOrigin: "0 0", scale: `${v}`, borderRadius: (34 * z) / v, overflow: "hidden", opacity: cardO, boxShadow: `0 ${20 * z}px ${60 * z}px rgba(20,20,30,${0.18 * z})` }}>
        <Sequence durationInFrames={Math.round(B_LEN * fps)}>
          <Video src={staticFile("reel_b.mp4")} muted style={{ width: 1440, height: 900 }} />
        </Sequence>
        <Sequence from={Math.round(B_LEN * fps)}>
          <Img src={staticFile("reel_last.jpg")} style={{ width: 1440, height: 900 }} />
        </Sequence>
      </div>
      <div style={{ position: "absolute", left: x, top: y, width: w, height: h, borderRadius: r, overflow: "hidden", background: "#f3f4f8", boxShadow: `0 ${24 * (1 - e)}px ${70 * (1 - e)}px rgba(10,10,20,${0.3 * (1 - e)})` }}>
        <div style={{ position: "absolute", left: DOX * dScale, top: 0, width: 1366, height: DH + 200, transformOrigin: "0 0", scale: `${dScale}`, opacity: deskO }}>
          <Desktop s={dState} height={DH} />
        </div>
        <div style={{ position: "absolute", left: 0, top: 0, transformOrigin: "0 0", scale: `${mScale}`, opacity: mobO }}>
          <Mobile open={open} height={h / mScale + 10} scroll={scroll} tap={{ x: 150, y: 296, q: tapQ }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

type Key = { t: number; x: number; y: number; click?: boolean };

export const DeskScene: React.FC<{ scale?: number; ox?: number; dh?: number; intro?: boolean; wipe?: boolean }> = ({ scale = DS, ox = DOX, dh = DH, intro = false, wipe = false }) => {
  const { fps } = useVideoConfig();
  const f = useCurrentFrame();
  const t = f / fps;
  const sp = (at: number) => spring({ frame: f - at * fps, fps, config: { damping: 200 } });
  const lin = (a: number, b: number) => interpolate(t, [a, b], [0, 1], { ...clamp, easing: inOut });
  const SH = intro ? 2.7 : 0;

  const WHY = { x: 560, y: L.cardsY + 24 + 56 + 16 + 22 };
  const REP = { x: 196, y: 376 };
  const modalH = 432;
  const mTop = (dh - modalH) / 2;
  const CHIP = { x: 465, y: mTop + 32 + 30 + 8 + 42 + 22 + 20 };
  const CTA = { x: 683, y: mTop + modalH - 32 - 27 };
  const REST = { x: 1010, y: 640 };
  const INPUT = { x: 1010, y: dh - 48 };
  const SEND = { x: 1198, y: dh - 48 };

  const keys: Key[] = [
    ...(intro ? [{ t: 0.4, ...REST }, { t: 1.3, ...WHY, click: true }, { t: 2.7, ...WHY }] : [{ t: 0.6, ...REST }]),
    { t: SH + 1.5, ...REP, click: true },
    { t: SH + 2.1, ...REP },
    { t: SH + 2.8, ...CHIP, click: true },
    { t: SH + 3.4, ...CHIP },
    { t: SH + 4.1, ...CTA, click: true },
    { t: SH + 7.9, ...REST },
    { t: SH + 8.7, ...WHY, click: true },
    { t: SH + 9.9, ...WHY },
    { t: SH + 10.6, ...INPUT, click: true },
    { t: SH + 12.0, ...INPUT },
    { t: SH + 12.6, ...SEND, click: true },
  ];
  let cx = keys[0].x;
  let cy = keys[0].y;
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i];
    const b = keys[i + 1];
    if (t >= a.t) {
      const k = interpolate(t, [a.t, b.t], [0, 1], { ...clamp, easing: inOut });
      cx = a.x + (b.x - a.x) * k;
      cy = a.y + (b.y - a.y) * k;
    }
  }
  const firstT = keys[0].t;
  const curO = t < firstT ? 0 : t > SH + 4.35 && t < SH + 7.8 ? 0 : 1;
  const lastClick = [...keys].reverse().find((k) => k.click && t >= k.t);
  const q = lastClick ? (t - lastClick.t) / 0.5 : -1;
  const set2 = t >= SH + 6.8;
  const s: DesktopState = {
    set: set2 ? 2 : 1,
    open: set2 ? sp(SH + 8.7) : intro ? sp(1.3) : 1,
    reveal: set2 ? interpolate(t, [SH + 6.8, SH + 7.8], [0, 3.2], { ...clamp, easing: ease }) : 3,
    modal: sp(SH + 1.5) - sp(SH + 4.1),
    chip: lin(SH + 2.8, SH + 3.05),
    loading: t >= SH + 4.35 && !set2 ? interpolate(t, [SH + 4.35, SH + 6.8], [0, 1], { ...clamp, easing: Easing.bezier(0.3, 0, 0.4, 1) }) : null,
    typing: set2 ? interpolate(t, [SH + 7.0, SH + 7.9], [0.01, 1], clamp) : 0,
    msg: set2 ? sp(SH + 7.9) : 1,
    shimmer: f,
    draft: interpolate(t, [SH + 10.75, SH + 11.95], [0, 1], clamp),
    sent: sp(SH + 12.65),
    reply: t > SH + 13.6 ? sp(SH + 13.6) : 0,
  };
  const wq = wipe ? interpolate(t, [SH + 14.5, SH + 15.6], [0, 1], { ...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1) }) : 0;
  return (
    <AbsoluteFill style={{ background: "#f3f4f8" }}>
      <div style={{ position: "absolute", left: ox * scale, top: 0, width: 1366, height: dh, transformOrigin: "0 0", scale: `${scale}` }}>
        <Desktop s={s} height={dh}>
          <Ripple x={lastClick?.x ?? 0} y={lastClick?.y ?? 0} q={curO ? q : -1} />
          <Cursor x={cx} y={cy} o={curO} />
          {wq > 0 ? <div style={{ position: "absolute", left: SEND.x - wq * 1700, top: SEND.y - wq * 1700, width: wq * 3400, height: wq * 3400, borderRadius: "50%", background: "#fa2a48", zIndex: 60 }} /> : null}
        </Desktop>
      </div>
    </AbsoluteFill>
  );
};

export const CaseClip: React.FC<{ intro: boolean }> = ({ intro }) => (
  <AbsoluteFill>
    <style>{fontCss}</style>
    <DeskScene scale={2000 / 1366} ox={0} dh={1196 / (2000 / 1366)} intro={intro} />
  </AbsoluteFill>
);

export const Cover: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <style>{fontCss}</style>
      <Sequence from={Math.round(TB * fps)} durationInFrames={Math.round((D0 - TB) * fps)}>
        <MockupScene />
      </Sequence>
      <Sequence from={Math.round(D0 * fps)}>
        <DeskScene wipe />
      </Sequence>
      <Sequence durationInFrames={Math.round(OP * fps)}>
        <Opener revealAt={REVEAL} />
      </Sequence>
    </AbsoluteFill>
  );
};
