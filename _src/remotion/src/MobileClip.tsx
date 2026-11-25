import React from "react";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Mobile } from "./ui/Mobile";
import { C, fontCss } from "./theme";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const inOut = Easing.bezier(0.65, 0, 0.35, 1);

const Ring: React.FC<{ at: number; period: number }> = ({ at, period }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = (((f / fps - at) % period) + period) % period / period;
  const r = 200 + k * 1100;
  return <div style={{ position: "absolute", left: 1000 - r, top: 598 - r, width: 2 * r, height: 2 * r, borderRadius: "50%", background: `radial-gradient(circle, rgba(255,255,255,0) 58%, rgba(255,255,255,${0.12 * (1 - k)}) 70%, rgba(255,255,255,0) 71%)` }} />;
};

/** Mobile web walkthrough on the brand background, loops seamlessly (rings are periodic, UI returns to start) */
export const MobileClip: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const W = 480;
  const H = 1060;
  const sc = 1;
  const scroll = interpolate(t, [1.0, 2.2], [0, 420], { ...clamp, easing: inOut }) - interpolate(t, [2.6, 3.4], [0, 420], { ...clamp, easing: inOut });
  const open = spring({ frame: f - 4.1 * fps, fps, config: { damping: 200 } }) - spring({ frame: f - 7.2 * fps, fps, config: { damping: 200 } });
  const tapQ = (t - 4.0) / 0.45;
  const tap2 = (t - 7.1) / 0.45;
  return (
    <AbsoluteFill style={{ background: C.brand, overflow: "hidden" }}>
      <style>{fontCss}</style>
      <Ring at={0} period={6} />
      <Ring at={2} period={6} />
      <Ring at={4} period={6} />
      <div style={{ position: "absolute", left: 1000 - (W * sc * 412 / 412) / 2, top: 68, width: W, height: H, borderRadius: 56, overflow: "hidden", boxShadow: "0 40px 90px rgba(90,0,20,.35)" }}>
        <div style={{ transformOrigin: "0 0", scale: `${W / 412}` }}>
          <Mobile open={Math.max(0, open)} height={H / (W / 412)} scroll={scroll} tap={{ x: 150, y: 296, q: tapQ >= 0 && tapQ <= 1 ? tapQ : tap2 }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};
