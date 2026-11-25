import React from "react";
import { C, SET1 } from "../theme";
import { Avatar, Spark, Star, Why } from "./Parts";

/** Mobile web screen, 412 px wide (design), no device frame */
export const Mobile: React.FC<{ open: number; height: number; scroll: number; tap?: { x: number; y: number; q: number } }> = ({ open, height, scroll, tap }) => (
  <div style={{ width: 412, height, background: C.dark, fontFamily: "Inter", color: C.ink, position: "relative", overflow: "hidden", fontFeatureSettings: '"cv11","ss03"' }}>
    <div style={{ padding: "30px 26px 0", color: "#fff" }}>
      <div style={{ fontFamily: "InterD", fontSize: 32, fontWeight: 600, letterSpacing: "-0.025em" }}>Biology</div>
      <div style={{ fontSize: 14, color: C.hint, marginTop: 4 }}>Exam prep, online, weekday evenings</div>
    </div>
    <div style={{ position: "absolute", left: 0, right: 0, top: 124, bottom: 0, background: "#fff", borderRadius: "28px 28px 0 0", overflow: "hidden" }}>
      <div style={{ padding: "22px 20px", translate: `0 ${-scroll}px` }}>
        <div style={{ fontFamily: "InterD", fontSize: 19, fontWeight: 600, letterSpacing: "-0.015em" }}>Best fit for your task</div>
        <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 13, color: C.ink2, marginTop: 4 }}>
          <Spark s={12} />
          Picked by AI from 12 offers
        </div>
        {SET1.map((t, i) => (
          <div key={t.id} style={{ marginTop: 18, paddingBottom: 18, borderBottom: `1px solid ${C.line}` }}>
            <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
              <Avatar img={t.img} size={46} online />
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 14.5, fontWeight: 600 }}>
                  {t.name}
                  <span style={{ display: "inline-flex", alignItems: "center", gap: 3, fontWeight: 400, color: C.ink2, fontSize: 12.5 }}>
                    <Star />
                    {t.rating}
                  </span>
                </div>
                <div style={{ fontFamily: "InterD", fontSize: 19, fontWeight: 600, letterSpacing: "-0.02em" }}>
                  {t.price} ₽ <span style={{ fontFamily: "Inter", fontSize: 12, fontWeight: 400, color: C.ink2, letterSpacing: 0 }}>per hour</span>
                </div>
              </div>
            </div>
            <div style={{ marginTop: 10 }}>
              <Why t={t} open={i === 0 ? open : 0} compact />
            </div>
            <div style={{ fontSize: 13, color: C.ink2, marginTop: 10 }}>{t.msg}</div>
          </div>
        ))}
        <div style={{ fontFamily: "InterD", fontSize: 17, fontWeight: 600, marginTop: 22 }}>Other offers</div>
        {[["Simon I.", "simon", "2,300"], ["Alex F.", "alex", "2,400"]].map(([n, img, p]) => (
          <div key={n} style={{ display: "flex", gap: 12, alignItems: "center", marginTop: 16 }}>
            <Avatar img={img} size={42} online />
            <div>
              <div style={{ fontSize: 14, fontWeight: 600 }}>{n}</div>
              <div style={{ fontSize: 14, color: C.ink2 }}>{p} ₽ per hour</div>
            </div>
          </div>
        ))}
      </div>
    </div>
    {tap && tap.q >= 0 && tap.q <= 1 ? (
      <div style={{ position: "absolute", left: tap.x - 22, top: tap.y - 22, width: 44, height: 44, borderRadius: "50%", background: `rgba(24,24,24,${0.18 * (1 - tap.q)})`, scale: `${0.5 + 0.8 * tap.q}` }} />
    ) : null}
  </div>
);
