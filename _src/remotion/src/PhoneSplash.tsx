import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { C } from "./theme";

/** Phone screen in the mom shot: brand red with slow concentric ripples, like rings on water */
export const PhoneSplash: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps + 2;
  const P = 5;
  const N = 5;
  return (
    <AbsoluteFill style={{ background: C.brand, overflow: "hidden" }}>
      {Array.from({ length: N }, (_, i) => {
        const k = ((((t - (i * P) / N) % P) + P) % P) / P;
        const r = 10 + k * 420;
        const a = 0.42 * Math.sin(Math.PI * Math.min(1, k * 1.15));
        return <div key={i} style={{ position: "absolute", left: 206 - r, top: 365 - r, width: 2 * r, height: 2 * r, borderRadius: "50%", background: `radial-gradient(circle closest-side, rgba(255,255,255,0) 45%, rgba(255,255,255,${Math.max(0, a) * 0.22}) 82%, rgba(255,255,255,${Math.max(0, a) * 0.5}) 97%, rgba(255,255,255,0) 100%)` }} />;
      })}
    </AbsoluteFill>
  );
};
