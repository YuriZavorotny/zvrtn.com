import React from "react";
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { C } from "./theme";

const CX = 720, CY = 450;
const EMIT: number[] = []; // ripples leave the dot while it sits in the centre
const LIFE = 2.6;
const MOVE = 1.0; // dot starts moving left and becomes the logo

const Ring: React.FC<{ at: number; fade: number }> = ({ at, fade }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = interpolate(f, [at * fps, (at + LIFE) * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.25, 0.6, 0.35, 1) });
  if (k <= 0 || k >= 1) return null;
  const r = 30 + k * 760;
  const a = 0.5 * (1 - k) * fade;
  return <div style={{ position: "absolute", left: CX - r, top: CY - 36 - r, width: 2 * r, height: 2 * r, borderRadius: "50%", background: `radial-gradient(circle closest-side, rgba(255,255,255,0) 45%, rgba(255,255,255,${a * 0.22}) 82%, rgba(255,255,255,${a * 0.5}) 97%, rgba(255,255,255,0) 100%)` }} />;
};

export const Opener: React.FC<{ revealAt: number }> = ({ revealAt }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dot = spring({ frame: f - 0.2 * fps, fps, config: { damping: 12, stiffness: 150 } });
  const shift = spring({ frame: f - MOVE * fps, fps, config: { damping: 200 }, durationInFrames: 0.9 * fps });
  const body = spring({ frame: f - (MOVE + 0.15) * fps, fps, config: { damping: 16 } });
  const fade = interpolate(f, [MOVE * fps, (MOVE + 0.5) * fps], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const letters = "PROFI".split("");
  const D = 236; // icon starts in the centre, ends at its place in the logo
  const rv = interpolate(f, [revealAt * fps, (revealAt + 0.7) * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.7, 0, 0.3, 1) });
  const R = rv * 1200;
  const mask = rv > 0 ? `radial-gradient(circle at ${CX - D}px ${CY}px, transparent ${R}px, #000 ${R + 1}px)` : undefined;
  return (
    <AbsoluteFill style={{ background: C.brand, WebkitMaskImage: mask, maskImage: mask }}>
      {EMIT.map((a) => (
        <Ring key={a} at={a} fade={fade} />
      ))}
      <div style={{ position: "absolute", left: 0, right: 0, top: CY - 60, height: 120, display: "flex", alignItems: "center", justifyContent: "center", gap: 40 }}>
        <div style={{ width: 116, height: 116, position: "relative", flex: "none", translate: `${D * (1 - shift)}px 0` }}>
          <div style={{ position: "absolute", left: 36, top: 0, width: 44, height: 44, borderRadius: "50%", background: "#fff", scale: `${dot}` }} />
          <div style={{ position: "absolute", left: 58 - 58 * body, top: 58, width: 116 * body, height: 56, borderRadius: 28, background: "#fff", opacity: body > 0.01 ? 1 : 0 }} />
        </div>
        <div style={{ display: "flex", overflow: "hidden", height: 130, alignItems: "center" }}>
          {letters.map((l, i) => {
            const k = spring({ frame: f - (MOVE + 0.25 + i * 0.07) * fps, fps, config: { damping: 18 } });
            return (
              <span key={i} style={{ fontFamily: "Mont", fontWeight: 700, fontSize: 132, lineHeight: 1, color: "#fff", display: "inline-block", translate: `0 ${(1 - k) * 140}px`, opacity: k > 0.01 ? 1 : 0 }}>
                {l}
              </span>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
