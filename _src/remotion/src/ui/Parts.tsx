import React from "react";
import { Img, interpolate, staticFile } from "remotion";
import { C, Tutor } from "../theme";

export const Spark: React.FC<{ s?: number; c?: string }> = ({ s = 14, c = C.aiStar }) => (
  <svg width={s} height={s} viewBox="0 0 24 24" style={{ flex: "none" }}>
    <path fill={c} d="M12 1.5l2.2 6.3 6.3 2.2-6.3 2.2L12 18.5l-2.2-6.3L3.5 10l6.3-2.2zM19.5 15l1 2.5 2.5 1-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1z" />
  </svg>
);

export const Check: React.FC<{ c?: string; s?: number }> = ({ c = C.ok, s = 12 }) => (
  <svg width={s} height={s} viewBox="0 0 24 24" style={{ flex: "none" }}>
    <path d="M4 12.5l5 5L20 6.5" fill="none" stroke={c} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export const Avatar: React.FC<{ img: string; size: number; online?: boolean }> = ({ img, size, online }) => (
  <div style={{ position: "relative", width: size, height: size, flex: "none" }}>
    <Img src={staticFile(`av/${img}.jpg`)} style={{ width: size, height: size, borderRadius: "50%", objectFit: "cover", display: "block" }} />
    {online ? (
      <div style={{ position: "absolute", right: 0, bottom: 1, width: size * 0.23, height: size * 0.23, borderRadius: "50%", background: C.ok, border: "2px solid #fff" }} />
    ) : null}
  </div>
);

/** AI explanation block. open: 0..1 (animated height of details) */
export const Why: React.FC<{ t: Tutor; open: number; compact?: boolean }> = ({ t, open, compact }) => {
  const fs = compact ? 13 : 14.5;
  const lh = compact ? 18 : 21;
  const extra = interpolate(open, [0, 1], [0, compact ? 70 : 150]);
  return (
    <div data-hl="why" style={{ background: C.ai, borderRadius: compact ? 12 : 14, padding: compact ? "10px 12px" : "13px 16px 14px", position: "relative" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 7, fontWeight: 600, fontSize: compact ? 13.5 : 15, letterSpacing: "-0.01em" }}>
        <Spark s={compact ? 13 : 15} />
        Why they fit you
      </div>
      <div style={{ fontSize: fs, lineHeight: `${lh}px`, marginTop: 4, paddingRight: 22, maxHeight: lh * (2 + open), overflow: "hidden", ...(open < 0.02 ? { display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical" as const } : {}) }}>{t.why}</div>
      <div style={{ maxHeight: extra, overflow: "hidden" }}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10, opacity: open }}>
          {t.crit.map((c) => (
            <span key={c} style={{ background: "#fff", borderRadius: 8, padding: compact ? "3px 8px" : "5px 10px", fontSize: compact ? 11.5 : 13, display: "inline-flex", alignItems: "center", gap: 6 }}>
              <Check s={compact ? 10 : 12} />
              {c}
            </span>
          ))}
        </div>
        {compact ? null : <div style={{ fontSize: 13, lineHeight: "18px", color: C.aiInk, marginTop: 10, opacity: open }}>{t.src}</div>}
      </div>
      <svg width={15} height={15} viewBox="0 0 24 24" style={{ position: "absolute", right: 14, top: compact ? 11 : 15, rotate: `${open * 180}deg` }}>
        <path d="M6 9l6 6 6-6" fill="none" stroke="#c98a10" strokeWidth={2.4} strokeLinecap="round" />
      </svg>
    </div>
  );
};

export const Star = () => (
  <svg width={13} height={13} viewBox="0 0 24 24">
    <path fill={C.aiStar} d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z" />
  </svg>
);

export const Cursor: React.FC<{ x: number; y: number; o: number; scale?: number }> = ({ x, y, o, scale = 1 }) => (
  <svg width={22 * scale} height={22 * scale} viewBox="0 0 24 24" style={{ position: "absolute", left: x - 3 * scale, top: y - 2 * scale, opacity: o, filter: "drop-shadow(0 1px 2px rgba(0,0,0,.35))", zIndex: 50 }}>
    <path d="M4 2l15 9-6.5 1.6L16 20l-3 1.4-3.5-7.5L4 18z" fill="#1a1a1a" stroke="#fff" strokeWidth={1.4} strokeLinejoin="round" />
  </svg>
);

export const Ripple: React.FC<{ x: number; y: number; q: number; scale?: number }> = ({ x, y, q, scale = 1 }) => {
  if (q < 0 || q > 1) return null;
  const s = 28 * scale;
  return <div style={{ position: "absolute", left: x - s / 2, top: y - s / 2, width: s, height: s, borderRadius: "50%", border: `${2 * scale}px solid #1a1a1a`, opacity: 0.8 * (1 - q), scale: `${0.3 + 1.3 * q}`, zIndex: 49 }} />;
};
