import React from "react";
import { interpolate } from "remotion";
import { C, SET1, SET2, Tutor } from "../theme";
import { Avatar, Spark, Star, Why } from "./Parts";

export type DesktopState = {
  set: 1 | 2;
  open: number; // first card explanation 0..1
  reveal: number; // 0..3 cards visible
  modal: number; // 0..1
  chip: number; // 0..1 "Cheaper" selected
  loading: number | null; // progress 0..1
  typing: number; // 0..1 typing indicator phase
  msg: number; // 0..1 chat message visible
  shimmer: number; // frame-based phase
  draft?: number;
  sent?: number;
  reply?: number;
  openAll?: boolean;
};

const W = 1366;
// Layout constants (design px), used for cursor targets
export const L = {
  colX: 412,
  colW: 440,
  cardsY: 166,
  whyCenter: { x: 412 + 24 + 150, y: 166 + 24 + 56 + 16 + 22 },
  repick: { x: 190, y: 388 },
  modalW: 540,
};
L.whyCenter.y = L.cardsY + 24 + 56 + 16 + 22;

const Card: React.FC<{ t: Tutor; open: number; tags?: boolean; style?: React.CSSProperties }> = ({ t, open, tags, style }) => (
  <div style={{ background: "#fff", borderRadius: 24, padding: 24, marginBottom: 10, ...style }}>
    <div style={{ display: "flex", gap: 14, alignItems: "center" }}>
      <Avatar img={t.img} size={56} online />
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 16, fontWeight: 600, letterSpacing: "-0.01em" }}>
          {t.name}
          <span style={{ display: "inline-flex", alignItems: "center", gap: 4, fontWeight: 400, color: C.ink2, fontSize: 14 }}>
            <Star />
            {t.rating}
            <span style={{ marginLeft: 6 }}>{t.reviews} reviews</span>
          </span>
        </div>
        <div style={{ fontFamily: "InterD", fontSize: 24, fontWeight: 600, letterSpacing: "-0.02em", marginTop: 2 }}>
          {t.price} ₽ <span style={{ fontFamily: "Inter", fontSize: 14, fontWeight: 400, color: C.ink2, letterSpacing: 0 }}>per hour</span>
        </div>
      </div>
    </div>
    <div style={{ marginTop: 16 }}>
      <Why t={t} open={open} tags={tags} />
    </div>
    <div style={{ display: "flex", justifyContent: "space-between", gap: 12, marginTop: 16, fontSize: 14.5, lineHeight: "20px" }}>
      <span>{t.msg}</span>
      <span style={{ fontSize: 12.5, color: C.hint }}>{t.time}</span>
    </div>
    {tags === undefined || open > 0.5 && !tags ? null : null}
    {tags !== undefined ? null : <div style={{ marginTop: 16, height: 46, borderRadius: 14, background: C.ctl, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, fontWeight: 600 }}>Reply</div>}
  </div>
);

const Skeleton: React.FC<{ p: number; shimmer: number }> = ({ p, shimmer }) => {
  const steps = ["Reading your task", "Comparing 12 offers with your request", "Checking reviews and prices", "Writing why each one fits"];
  const st = steps[Math.min(3, Math.floor(p * 4))];
  const sh = (shimmer % 60) / 60;
  const bgS = `linear-gradient(90deg, #eef0f5 ${sh * 100 - 30}%, #f8f9fb ${sh * 100}%, #eef0f5 ${sh * 100 + 30}%)`;
  return (
    <div style={{ background: "#fff", borderRadius: 24, padding: 24 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 17, fontWeight: 600 }}>
        <Spark s={18} />
        Picking the best specialists for you
      </div>
      <div style={{ fontSize: 14, color: C.ink2, marginTop: 6 }}>{st}…</div>
      <div style={{ height: 4, borderRadius: 2, background: C.ctl, marginTop: 18, overflow: "hidden" }}>
        <div style={{ height: 4, width: `${6 + p * 94}%`, borderRadius: 2, background: `linear-gradient(90deg,#ffb84d,${C.brand})` }} />
      </div>
      {[0, 1, 2].map((i) => (
        <div key={i} style={{ display: "flex", gap: 14, marginTop: 26 }}>
          <div style={{ width: 56, height: 56, borderRadius: "50%", background: bgS }} />
          <div style={{ flex: 1 }}>
            <div style={{ height: 14, width: "52%", borderRadius: 7, background: bgS }} />
            <div style={{ height: 22, width: "34%", borderRadius: 8, background: bgS, marginTop: 9 }} />
            <div style={{ height: 62, borderRadius: 14, background: bgS, marginTop: 16 }} />
          </div>
        </div>
      ))}
    </div>
  );
};

export const Chat: React.FC<{ t: Tutor; typing: number; msg: number; h: number; draft?: number; sent?: number; reply?: number }> = ({ t, typing, msg, h, draft = 0, sent = 0, reply = 0 }) => {
  const MINE = "Thursday at 6 pm works for me";
  const shown = sent > 0.02 ? "" : MINE.slice(0, Math.round(draft * MINE.length));
  return (
  <div style={{ background: "#fff", borderRadius: "24px 24px 0 0", height: h, position: "relative", overflow: "hidden" }}>
    <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "20px 24px", borderBottom: `1px solid ${C.line}` }}>
      <Avatar img={t.img} size={46} online />
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 16.5, fontWeight: 600, letterSpacing: "-0.01em" }}>{t.name}</div>
        <div style={{ fontSize: 13.5, color: typing > 0 && msg < 0.05 ? C.ink2 : C.ok, marginTop: 2 }}>{typing > 0 && msg < 0.05 ? "typing…" : "Online"}</div>
      </div>
      <svg width={20} height={20} viewBox="0 0 24 24"><path d="M9 4h6l-1 6 4 3v2h-5v6l-1 1-1-1v-6H6v-2l4-3z" fill="none" stroke={C.hint} strokeWidth={1.6} strokeLinejoin="round" /></svg>
    </div>
    <div style={{ padding: "22px 24px" }}>
      <div style={{ textAlign: "center", fontSize: 12.5, color: C.hint, marginBottom: 16 }}>Today</div>
      <div style={{ display: "flex", gap: 6, alignItems: "center", background: C.ctl, borderRadius: "18px 18px 18px 6px", padding: "12px 16px", width: 64, opacity: typing * (1 - msg), position: msg < 1 ? "relative" : "absolute", height: msg < 1 ? undefined : 0 }}>
        {[0, 1, 2].map((i) => <span key={i} style={{ width: 7, height: 7, borderRadius: "50%", background: C.hint, opacity: 0.4 + 0.6 * Math.abs(Math.sin(typing * 12 + i)) }} />)}
      </div>
      <div style={{ background: C.ctl, borderRadius: "18px 18px 18px 6px", padding: "13px 16px", fontSize: 15, lineHeight: "22px", maxWidth: 300, opacity: msg, translate: `0 ${(1 - msg) * 10}px` }}>
        Hi! I’ve read your request: {t.id === "a" ? "biology exam in June, online, weekday evenings." : "cheaper lessons, online, weekday evenings."} I’m free on Tuesdays and Thursdays from 6 pm.
        <div style={{ marginTop: 8 }}>Shall we start with a short call?</div>
        <div style={{ textAlign: "right", fontSize: 12, color: C.hint, marginTop: 2 }}>{t.time}</div>
      </div>
      {sent > 0 ? (
        <div style={{ marginTop: 10, marginLeft: "auto", width: "fit-content", background: C.ink, color: "#fff", borderRadius: "18px 18px 6px 18px", padding: "12px 16px", fontSize: 15, lineHeight: "22px", opacity: sent, translate: `0 ${(1 - sent) * 12}px` }}>
          {MINE}
          <div style={{ textAlign: "right", fontSize: 12, color: "#8f909a", marginTop: 2 }}>04:31</div>
        </div>
      ) : null}
      {reply > 0 ? (
        <div style={{ marginTop: 10, width: "fit-content", background: C.ctl, borderRadius: "18px 18px 18px 6px", padding: "12px 16px", fontSize: 15, lineHeight: "22px", opacity: reply, translate: `0 ${(1 - reply) * 12}px` }}>
          Great, see you on Thursday! I’ll send a link before the call.
          <div style={{ textAlign: "right", fontSize: 12, color: C.hint, marginTop: 2 }}>04:32</div>
        </div>
      ) : null}
    </div>
    <div style={{ position: "absolute", left: 24, right: 24, bottom: 24, height: 48, borderRadius: 14, background: C.ctl, display: "flex", alignItems: "center", padding: "0 6px 0 16px", fontSize: 15, color: shown ? C.ink : C.hint }}>
      <span style={{ flex: 1 }}>{shown || "Message"}{draft > 0 && !sent ? <span style={{ display: "inline-block", width: 1.5, height: 18, background: C.ink, marginLeft: 1, verticalAlign: "-3px" }} /> : null}</span>
      <span style={{ width: 36, height: 36, borderRadius: 10, background: draft > 0 && !sent ? C.brand : "#dfe1ea", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <svg width={16} height={16} viewBox="0 0 24 24"><path d="M12 19V5M5.5 11.5L12 5l6.5 6.5" fill="none" stroke="#fff" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" /></svg>
      </span>
    </div>
  </div>
  );
};

const Modal: React.FC<{ t: number; chip: number }> = ({ t, chip }) => {
  if (t <= 0.001) return null;
  const chips = ["Cheaper", "More experience", "Later in the evening", "Female tutor"];
  return (
    <div style={{ position: "absolute", inset: 0, background: `rgba(24,24,24,${0.42 * t})`, display: "flex", alignItems: "center", justifyContent: "center", zIndex: 20 }}>
      <div style={{ width: L.modalW, background: "#fff", borderRadius: 28, padding: 32, opacity: t, translate: `0 ${(1 - t) * 24}px`, scale: `${0.97 + 0.03 * t}` }}>
        <div style={{ fontFamily: "InterD", fontSize: 24, fontWeight: 600, letterSpacing: "-0.02em" }}>What would you like to change?</div>
        <div style={{ fontSize: 15, lineHeight: "21px", color: C.ink2, margin: "8px 0 22px" }}>Pick a hint or say it in your own words. We’ll find three new specialists.</div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {chips.map((c, i) => (
            <div key={c} id={`chip${i}`} style={{ height: 40, borderRadius: 20, padding: "0 16px", display: "flex", alignItems: "center", fontSize: 15, background: i === 0 ? `rgb(${interpolate(chip, [0, 1], [239, 24])},${interpolate(chip, [0, 1], [241, 24])},${interpolate(chip, [0, 1], [248, 24])})` : C.ctl, color: i === 0 && chip > 0.5 ? "#fff" : C.ink }}>
              {c}
            </div>
          ))}
        </div>
        <div style={{ marginTop: 16, border: "1.5px solid #e3e5ee", borderRadius: 16, padding: "14px 16px", fontSize: 15.5, lineHeight: "23px", minHeight: 104 }}>
          Biology exam in June, online lessons on weekday evenings,{" "}
          <span style={{ position: "relative" }}>
            <span style={{ opacity: 1 - chip }}>budget up to 2,500 ₽ per hour</span>
            <span style={{ position: "absolute", left: 0, top: 0, whiteSpace: "nowrap", opacity: chip, background: "#ffe9b3", borderRadius: 5, padding: "0 4px", margin: "0 -4px" }}>cheaper, up to 1,500 ₽ per hour</span>
          </span>
        </div>
        <div style={{ marginTop: 22, height: 54, borderRadius: 16, background: C.brand, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16.5, fontWeight: 600 }}>Find other pros</div>
      </div>
    </div>
  );
};

export const Desktop: React.FC<{ s: DesktopState; height: number; children?: React.ReactNode }> = ({ s, height, children }) => {
  const set = s.set === 1 ? SET1 : SET2;
  const menu: [string, boolean, string][] = [
    ["Order details", false, "M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"],
    ["Offers", true, "M12 3a9 9 0 100 18 9 9 0 000-18zM8 12.5l2.5 2.5L16 9.5"],
    ["All specialists", false, "M9 4.5a3.5 3.5 0 100 7 3.5 3.5 0 000-7zM2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5M16 4.8a3.5 3.5 0 010 6.4M18.5 14.8c1.6.8 2.7 2.5 3 5.2"],
  ];
  return (
    <div style={{ position: "relative", width: W, height, background: C.bg, fontFamily: "Inter", color: C.ink, overflow: "hidden", fontFeatureSettings: '"cv11","ss03"' }}>
      <div style={{ position: "absolute", left: 120, top: 32, fontFamily: "Mont", fontWeight: 700, fontSize: 22, color: C.brand, letterSpacing: "0.01em" }}>PROFI</div>
      <div style={{ position: "absolute", right: 120, top: 24, display: "flex", alignItems: "center", gap: 22, fontSize: 14.5, color: C.ink2 }}>
        <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <svg width={20} height={20} viewBox="0 0 24 24"><path d="M4 12a8 8 0 1 1 3.3 6.5L3 20l1.2-4A8 8 0 0 1 4 12z" fill="none" stroke={C.ink2} strokeWidth={1.7} /></svg>
          Messages
          <span style={{ background: C.brand, color: "#fff", fontSize: 11.5, fontWeight: 600, minWidth: 20, height: 20, borderRadius: 10, display: "inline-flex", alignItems: "center", justifyContent: "center" }}>3</span>
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <svg width={20} height={20} viewBox="0 0 24 24"><path d="M12 20.5s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.7c0 5.6-7.5 10.2-7.5 10.2z" fill="none" stroke={C.ink2} strokeWidth={1.7} /></svg>
          Favourites
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: 10, color: C.ink }}>
          <Avatar img="daniel" size={32} />
          Daniel K.
        </span>
      </div>
      {/* sidebar */}
      <div style={{ position: "absolute", left: 120, top: 98, width: 250 }}>
        <div style={{ fontFamily: "InterD", fontSize: 34, fontWeight: 600, letterSpacing: "-0.025em", marginBottom: 24 }}>Biology</div>
        {menu.map(([t, on, d]) => (
          <div key={t} style={{ display: "flex", alignItems: "center", gap: 12, height: 48, margin: "0 -14px", padding: "0 14px", borderRadius: 14, fontSize: 15.5, background: on ? "#e6e8f0" : "transparent", fontWeight: on ? 600 : 400 }}>
            <svg width={18} height={18} viewBox="0 0 24 24">
              <path d={d} fill="none" stroke={C.ink} strokeWidth={1.7} strokeLinecap="round" />
            </svg>
            {t}
            {on ? <span style={{ marginLeft: "auto", background: C.brand, color: "#fff", fontSize: 12, fontWeight: 600, minWidth: 22, height: 22, borderRadius: 11, display: "inline-flex", alignItems: "center", justifyContent: "center" }}>12</span> : null}
          </div>
        ))}
        <div style={{ height: 1, background: "#dfe1ea", margin: "22px 0 18px" }} />
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", height: 60 }}>
          <div>
            <div style={{ fontSize: 15.5, fontWeight: 600 }}>Find other pros</div>
            <div style={{ fontSize: 13.5, color: C.ink2, marginTop: 2 }}>Tell us what to change</div>
          </div>
          <div style={{ width: 36, height: 36, borderRadius: 11, background: C.ink, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <svg width={18} height={18} viewBox="0 0 24 24">
              <path d="M4 7h10M18 7h2M4 17h2M10 17h10" stroke="#fff" strokeWidth={1.8} strokeLinecap="round" />
              <circle cx={16} cy={7} r={2} fill="none" stroke="#fff" strokeWidth={1.8} />
              <circle cx={8} cy={17} r={2} fill="none" stroke="#fff" strokeWidth={1.8} />
            </svg>
          </div>
        </div>
      </div>
      {/* middle column */}
      <div style={{ position: "absolute", left: L.colX, top: 98, width: L.colW }}>
        <div style={{ height: 68 }}>
          {s.loading === null ? (
            <>
              <div style={{ fontFamily: "InterD", fontSize: 22, fontWeight: 600, letterSpacing: "-0.015em" }}>Best fit for your task</div>
              <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 14, color: C.ink2, marginTop: 5 }}>
                <Spark s={13} />
                {s.set === 1 ? "Picked by AI from 12 offers" : "New pick: cheaper, same goals"}
              </div>
            </>
          ) : null}
        </div>
        {s.loading !== null ? (
          <Skeleton p={s.loading} shimmer={s.shimmer} />
        ) : (
          set.map((t, i) => {
            const k = Math.max(0, Math.min(1, s.reveal - i));
            return <Card key={t.id} t={t} open={i === 0 ? s.open : 0} tags={s.openAll ? i > 0 : undefined} style={{ opacity: k, translate: `0 ${(1 - k) * 18}px` }} />;
          })
        )}
      </div>
      {/* right column */}
      <div style={{ position: "absolute", left: 868, top: 166, width: 378 }}>
        <Chat t={set[0]} typing={s.typing} msg={s.msg} h={height - 166} draft={s.draft} sent={s.sent} reply={s.reply} />
      </div>
      <Modal t={s.modal} chip={s.chip} />
      {children}
    </div>
  );
};
