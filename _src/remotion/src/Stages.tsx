import React from "react";
import { AbsoluteFill } from "remotion";
import { C, SET1, Tutor, fontCss } from "./theme";
import { Avatar, Check, Spark, Star, Why } from "./ui/Parts";
import { Desktop } from "./ui/Desktop";

/* Static screens for the four design stages. Desktop 1366x800, mobile web 393x852. English, anonymised. */

type Row = { name: string; img: string; rating: string; reviews: number; msg: string; unread?: number; price?: string };
const ROWS: Row[] = [
  { name: "Olivia M.", img: "olivia", rating: "5.0", reviews: 54, msg: "Happy to start with a short call to plan your prep", unread: 1, price: "2,200" },
  { name: "Victoria B.", img: "victoria", rating: "4.8", reviews: 43, msg: "Let’s set up a call to go through your task", unread: 2, price: "2,100" },
  { name: "Anna F.", img: "anna", rating: "4.9", reviews: 133, msg: "Ready to meet and talk through your request", unread: 1, price: "2,400" },
  { name: "Simon I.", img: "simon", rating: "4.6", reviews: 24, msg: "Good afternoon, I’d be glad to take your order", unread: 1, price: "2,300" },
  { name: "Helen T.", img: "helen", rating: "4.8", reviews: 55, msg: "Hello, I can start as early as next week", price: "1,900" },
  { name: "Alex F.", img: "alex", rating: "4.7", reviews: 10, msg: "I fully understand what you need for the exam", price: "2,400" },
];
const PRAISE = [
  ["Explains clearly", "Exam results", "Patient"],
  ["Structured lessons", "Past papers", "Punctual"],
  ["Finds the gaps", "Flexible schedule", "Calm"],
];
const WHY3 = [
  "Asks what your goal is for the exam and where you get stuck, and takes time to understand your situation before suggesting a plan.",
  "13 years preparing students for the biology exam. Works through past exam papers to build speed and confidence.",
  "Suggests clarifying what is hard for you before lessons start. Doesn’t push a ready-made programme.",
];

const Badge: React.FC<{ n: number }> = ({ n }) => (
  <span style={{ background: C.brand, color: "#fff", fontSize: 11.5, fontWeight: 600, minWidth: 20, height: 20, borderRadius: 10, display: "inline-flex", alignItems: "center", justifyContent: "center", flex: "none" }}>{n}</span>
);
const Meta: React.FC<{ r: Row; fs?: number }> = ({ r, fs = 13 }) => (
  <span style={{ display: "inline-flex", alignItems: "center", gap: 4, color: C.ink2, fontSize: fs, fontWeight: 400 }}>
    <Star />
    {r.rating}
    <svg width={13} height={13} viewBox="0 0 24 24" style={{ marginLeft: 6 }}><path d="M4 12a8 8 0 1 1 3.3 6.5L3 20l1.2-4A8 8 0 0 1 4 12z" fill="none" stroke={C.ink2} strokeWidth={2} /></svg>
    {r.reviews}
  </span>
);
const Verified = () => (
  <svg width={15} height={15} viewBox="0 0 24 24" style={{ flex: "none" }}><circle cx={12} cy={12} r={10} fill={C.ok} /><path d="M7.5 12.3l3 3 6-6.3" fill="none" stroke="#fff" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" /></svg>
);
const ListRow: React.FC<{ r: Row; sel?: boolean; m?: boolean; praise?: string[] }> = ({ r, sel, m, praise }) => (
  <div style={{ display: "flex", gap: 12, padding: m ? "12px 0" : "12px 14px", margin: m ? 0 : "0 -6px", borderRadius: 16, background: sel ? "rgba(4,4,15,0.05)" : "transparent" }}>
    <Avatar img={r.img} size={m ? 48 : 46} online />
    <div style={{ flex: 1, minWidth: 0 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: m ? 15 : 14.5, fontWeight: 600 }}>
        {r.name}
        <Verified />
      </div>
      <div style={{ marginTop: 2 }}><Meta r={r} /></div>
      {praise ? (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginTop: 7, alignItems: "center" }}>
          <span style={{ fontSize: 12.5, color: C.ink2, marginRight: 2 }}>Praised for</span>
          {praise.map((p) => <span key={p} style={{ fontSize: 12, padding: "3px 8px", borderRadius: 7, background: "#e7f6ee", color: "#0f7a4c" }}>{p}</span>)}
        </div>
      ) : null}
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 6 }}>
        <span style={{ flex: 1, fontSize: 13.5, color: C.ink2, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{r.msg}</span>
        {r.unread ? <Badge n={r.unread} /> : null}
      </div>
    </div>
  </div>
);

const MENU: [string, string][] = [
  ["Order details", "M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"],
  ["Offers", "M12 3a9 9 0 100 18 9 9 0 000-18zM8 12.5l2.5 2.5L16 9.5"],
  ["All specialists", "M9 4.5a3.5 3.5 0 100 7 3.5 3.5 0 000-7zM2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5M16 4.8a3.5 3.5 0 010 6.4M18.5 14.8c1.6.8 2.7 2.5 3 5.2"],
];
const Repick: React.FC = () => (
  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", height: 60 }}>
    <div>
      <div style={{ fontSize: 15.5, fontWeight: 600 }}>Find other pros</div>
      <div style={{ fontSize: 13.5, color: C.ink2, marginTop: 2 }}>Tell us what to change</div>
    </div>
    <div style={{ width: 36, height: 36, borderRadius: 11, background: C.ink, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <svg width={18} height={18} viewBox="0 0 24 24"><path d="M4 7h10M18 7h2M4 17h2M10 17h10" stroke="#fff" strokeWidth={1.8} strokeLinecap="round" /><circle cx={16} cy={7} r={2} fill="none" stroke="#fff" strokeWidth={1.8} /><circle cx={8} cy={17} r={2} fill="none" stroke="#fff" strokeWidth={1.8} /></svg>
    </div>
  </div>
);
const Toggle: React.FC = () => (
  <div>
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", fontSize: 14.5, fontWeight: 600 }}>
      Receive offers
      <span style={{ width: 40, height: 24, borderRadius: 12, background: C.ok, position: "relative" }}><span style={{ position: "absolute", right: 3, top: 3, width: 18, height: 18, borderRadius: 9, background: "#fff" }} /></span>
    </div>
    <div style={{ fontSize: 13, color: C.ink2, marginTop: 6, lineHeight: "18px" }}>Specialists see your order and can send offers</div>
  </div>
);

const ChatPane: React.FC<{ r: Row; text: string }> = ({ r, text }) => (
  <div style={{ background: "#fff", borderRadius: 24, height: 702, position: "relative", overflow: "hidden" }}>
    <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "20px 24px", borderBottom: `1px solid ${C.line}` }}>
      <Avatar img={r.img} size={46} online />
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 16.5, fontWeight: 600 }}>{r.name}</div>
        <div style={{ fontSize: 13.5, color: C.ok, marginTop: 2 }}>Online</div>
      </div>
    </div>
    <div style={{ padding: "22px 24px" }}>
      <div style={{ textAlign: "center", fontSize: 12.5, color: C.hint, marginBottom: 16 }}>Today</div>
      <div style={{ background: C.ctl, borderRadius: "18px 18px 18px 6px", padding: "13px 16px", fontSize: 15, lineHeight: "22px", maxWidth: 300 }}>
        {text}
        <div style={{ textAlign: "right", fontSize: 12, color: C.hint, marginTop: 2 }}>07:20</div>
      </div>
    </div>
    <div style={{ position: "absolute", left: 24, right: 24, bottom: 24, height: 48, borderRadius: 14, background: C.ctl, display: "flex", alignItems: "center", padding: "0 16px", fontSize: 15, color: C.hint }}>Message</div>
  </div>
);

const DeskShell: React.FC<{ side: React.ReactNode; mid: React.ReactNode; right: React.ReactNode; overlay?: React.ReactNode }> = ({ side, mid, right, overlay }) => (
  <div style={{ position: "relative", width: 1366, height: 800, background: C.bg, fontFamily: "Inter", color: C.ink, overflow: "hidden", fontFeatureSettings: '"cv11","ss03"' }}>
    <div style={{ position: "absolute", left: 120, top: 32, fontFamily: "Mont", fontWeight: 700, fontSize: 22, color: C.brand }}>PROFI</div>
    <div style={{ position: "absolute", right: 120, top: 24, display: "flex", alignItems: "center", gap: 10, fontSize: 14.5 }}>
      <Avatar img="daniel" size={32} />
      Daniel K.
    </div>
    <div style={{ position: "absolute", left: 120, top: 98, width: 250 }}>
      <div style={{ fontFamily: "InterD", fontSize: 34, fontWeight: 600, letterSpacing: "-0.025em", marginBottom: 24 }}>Biology</div>
      {MENU.map(([t, d], i) => (
        <div key={t} style={{ display: "flex", alignItems: "center", gap: 12, height: 48, margin: "0 -14px", padding: "0 14px", borderRadius: 14, fontSize: 15.5, background: i === 1 ? "#e6e8f0" : "transparent", fontWeight: i === 1 ? 600 : 400 }}>
          <svg width={18} height={18} viewBox="0 0 24 24"><path d={d} fill="none" stroke={C.ink} strokeWidth={1.7} strokeLinecap="round" /></svg>
          {t}
          {i === 1 ? <span style={{ marginLeft: "auto" }}><Badge n={9} /></span> : null}
        </div>
      ))}
      <div style={{ height: 1, background: "#dfe1ea", margin: "22px 0 18px" }} />
      {side}
    </div>
    <div style={{ position: "absolute", left: 412, top: 98, width: 440, height: 702, overflow: "hidden" }}>{mid}</div>
    <div style={{ position: "absolute", left: 868, top: 98, width: 378 }}>{right}</div>
    {overlay}
  </div>
);

const Head: React.FC<{ t: string; s: string; ai?: boolean; n?: string }> = ({ t, s, ai, n }) => (
  <div style={{ marginBottom: 14 }}>
    <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", fontFamily: "InterD", fontSize: 22, fontWeight: 600, letterSpacing: "-0.015em" }}>
      {t}
      {n ? <span style={{ fontFamily: "Inter", fontSize: 16, fontWeight: 400, color: C.hint }}>{n}</span> : null}
    </div>
    <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 14, color: C.ink2, marginTop: 5 }}>
      {ai ? <Spark s={13} /> : null}
      {s}
    </div>
  </div>
);

const LlmCard: React.FC<{ r: Row; why: string; m?: boolean }> = ({ r, why, m }) => (
  <div style={{ background: "#fff", borderRadius: m ? 22 : 24, padding: m ? 18 : 22, marginBottom: 10 }}>
    <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
      <Avatar img={r.img} size={m ? 48 : 52} online />
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 15, fontWeight: 600 }}>{r.name}<Meta r={r} /></div>
        <div style={{ fontFamily: "InterD", fontSize: m ? 21 : 23, fontWeight: 600, letterSpacing: "-0.02em", marginTop: 2 }}>
          {r.price} ₽ <span style={{ fontFamily: "Inter", fontSize: 13, fontWeight: 400, color: C.ink2 }}>per hour</span>
        </div>
      </div>
    </div>
    <div style={{ background: C.ai, borderRadius: 14, padding: "12px 14px", marginTop: 14 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 7, fontWeight: 600, fontSize: 14.5 }}><Spark s={14} />Why they fit you</div>
      <div style={{ fontSize: 14, lineHeight: "20px", marginTop: 4, display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>{why}</div>
    </div>
    <div style={{ fontSize: 14, lineHeight: "20px", marginTop: 12, display: "flex", gap: 10 }}><span style={{ flex: 1 }}>{r.msg}</span>{r.unread ? <Badge n={r.unread} /> : null}</div>
    <div style={{ marginTop: 12, height: 42, borderRadius: 13, background: C.ctl, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14.5, fontWeight: 600 }}>Reply</div>
  </div>
);

/* ---------- desktop per stage ---------- */
const desk1 = (
  <DeskShell
    side={<Toggle />}
    mid={
      <div style={{ background: "#fff", borderRadius: 24, padding: "20px 20px 8px" }}>
        <div style={{ fontFamily: "InterD", fontSize: 20, fontWeight: 600, marginBottom: 12 }}>Offers <span style={{ color: C.hint, fontFamily: "Inter", fontWeight: 400 }}>9</span></div>
        <div style={{ background: C.ctl, borderRadius: 18, padding: "12px 8px 6px", marginBottom: 6 }}>
          <div style={{ display: "flex", justifyContent: "space-between", padding: "0 8px 4px" }}>
            <div>
              <div style={{ fontSize: 13.5, fontWeight: 600 }}>Best match for your task</div>
              <div style={{ fontSize: 12.5, color: C.ink2, marginTop: 1 }}>Great reviews on similar tasks</div>
            </div>
            <svg width={18} height={18} viewBox="0 0 24 24"><path d="M7 21H4V10h3zM7 10l4-7c1.7 0 2.5 1 2.2 2.7L12.6 9H19a2 2 0 0 1 2 2.3l-1.3 7.5A2.6 2.6 0 0 1 17.1 21H7" fill={C.hint} /></svg>
          </div>
          {ROWS.slice(0, 3).map((r, i) => <ListRow key={r.name} r={r} sel={i === 0} />)}
        </div>
        {ROWS.slice(3).map((r) => <ListRow key={r.name} r={r} />)}
      </div>
    }
    right={<ChatPane r={ROWS[0]} text="Happy to start with a short call to plan your prep. When is the exam?" />}
  />
);

const desk2 = (
  <DeskShell
    side={<Repick />}
    mid={
      <div style={{ background: "#fff", borderRadius: 24, padding: "22px 20px 10px" }}>
        <Head t="Best fit for your task" s="Top by experience and reviews" />
        {ROWS.slice(0, 3).map((r, i) => <ListRow key={r.name} r={r} sel={i === 0} praise={PRAISE[i]} />)}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", borderTop: `1px solid ${C.line}`, margin: "10px 0 0", padding: "16px 2px 8px" }}>
          <span style={{ fontSize: 15.5, fontWeight: 600 }}>More specialists</span>
          <span style={{ fontSize: 13.5, fontWeight: 600, background: C.ctl, borderRadius: 10, padding: "7px 12px" }}>Show 6</span>
        </div>
      </div>
    }
    right={<ChatPane r={ROWS[0]} text="Happy to start with a short call to plan your prep. When is the exam?" />}
  />
);

const desk3 = (
  <DeskShell
    side={<Repick />}
    mid={
      <>
        <Head t="Best for your task" s="Matched by experience and reviews" ai />
        {ROWS.slice(0, 3).map((r, i) => <LlmCard key={r.name} r={r} why={WHY3[i]} />)}
      </>
    }
    right={<ChatPane r={ROWS[0]} text="Happy to start with a short call to plan your prep. When is the exam?" />}
  />
);

const desk4 = <Desktop s={{ set: 1, open: 1, reveal: 3, modal: 0, chip: 0, loading: null, typing: 1, msg: 1, shimmer: 0 }} height={800} />;

/* ---------- mobile web ---------- */
const TABS: [string, string][] = [["Order", "M12 4a8 8 0 100 16 8 8 0 000-16z"], ["All pros", "M9 5a3 3 0 100 6 3 3 0 000-6zM3 19c.8-3 3.2-4.5 6-4.5s5.2 1.5 6 4.5M16 5.5a3 3 0 010 5.5M18 14.5c1.5.7 2.5 2 2.8 4.5"], ["Offers", "M4 5h16v11H9l-5 4z"], ["Support", "M12 3a9 9 0 100 18 9 9 0 000-18zM9.5 9.5a2.5 2.5 0 114 2c-1 .6-1.5 1.1-1.5 2.2M12 17h.01"]];
const Phone: React.FC<{ children: React.ReactNode; overlay?: React.ReactNode; bg?: string }> = ({ children, overlay, bg = "#fff" }) => (
  <div style={{ position: "relative", width: 393, height: 852, background: bg, fontFamily: "Inter", color: C.ink, overflow: "hidden", fontFeatureSettings: '"cv11","ss03"' }}>
    <div style={{ height: 54, display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 32px 0 40px", fontSize: 16, fontWeight: 600, background: "#fff" }}>
      9:41
      <span style={{ display: "flex", gap: 6, alignItems: "center" }}>
        <svg width={18} height={12} viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1" fill={C.ink} /><rect x="5" y="5.5" width="3" height="6.5" rx="1" fill={C.ink} /><rect x="10" y="3" width="3" height="9" rx="1" fill={C.ink} /><rect x="15" y="0" width="3" height="12" rx="1" fill={C.ink} /></svg>
        <span style={{ width: 25, height: 12, borderRadius: 4, border: `1.5px solid ${C.ink}`, padding: 1.5, display: "inline-block" }}><span style={{ display: "block", width: "70%", height: "100%", borderRadius: 2, background: C.ink }} /></span>
      </span>
    </div>
    <div style={{ background: "#fff", padding: "6px 20px 0" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontFamily: "Mont", fontWeight: 700, fontSize: 19, color: C.brand }}>PROFI</span>
        <Avatar img="daniel" size={28} />
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: 12, borderBottom: `1px solid ${C.line}` }}>
        {TABS.map(([t, d], i) => (
          <div key={t} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4, padding: "0 6px 10px", fontSize: 12, color: i === 2 ? C.ink : C.ink2, fontWeight: i === 2 ? 600 : 400, borderBottom: i === 2 ? `2px solid ${C.ink}` : "2px solid transparent" }}>
            <svg width={22} height={22} viewBox="0 0 24 24"><path d={d} fill={i === 2 ? C.ink : "none"} stroke={i === 2 ? C.ink : C.ink2} strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round" /></svg>
            {t}
          </div>
        ))}
      </div>
    </div>
    <div style={{ position: "absolute", left: 0, right: 0, top: 150, bottom: 0, overflow: "hidden" }}>{children}</div>
    {overlay}
  </div>
);

const Sheet: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div style={{ position: "absolute", inset: 0, background: "rgba(24,24,24,.45)", display: "flex", alignItems: "flex-end" }}>
    <div style={{ width: "100%", background: "#fff", borderRadius: "28px 28px 0 0", padding: "14px 20px 34px" }}>
      <div style={{ width: 40, height: 5, borderRadius: 3, background: "#dfe1ea", margin: "0 auto 18px" }} />
      {children}
    </div>
  </div>
);
const Btn: React.FC<{ t: string }> = ({ t }) => (
  <div style={{ marginTop: 20, height: 52, borderRadius: 16, background: C.brand, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, fontWeight: 600 }}>{t}</div>
);

const mob1 = (
  <Phone>
    <div style={{ background: C.bg, padding: "12px 0" }}>
      <div style={{ background: "#fff", padding: "14px 20px", display: "flex", justifyContent: "space-between", alignItems: "center", borderRadius: "0 0 22px 22px" }}><Toggle /></div>
      <div style={{ background: "#fff", borderRadius: 22, marginTop: 10, padding: "16px 12px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 17, fontWeight: 600, padding: "0 8px 10px" }}>Offers <span style={{ color: C.hint, fontWeight: 400 }}>9</span></div>
        <div style={{ background: C.ctl, borderRadius: 18, padding: "12px 12px 2px" }}>
          <div style={{ fontSize: 13, fontWeight: 600 }}>Best match for your task</div>
          <div style={{ fontSize: 12, color: C.ink2, marginTop: 1 }}>Great reviews on similar tasks</div>
          {ROWS.slice(0, 3).map((r) => <ListRow key={r.name} r={r} m />)}
        </div>
        <div style={{ padding: "0 12px" }}>{ROWS.slice(3, 5).map((r) => <ListRow key={r.name} r={r} m />)}</div>
      </div>
    </div>
  </Phone>
);

const mob2 = (
  <Phone
    overlay={
      <Sheet>
        <div style={{ fontFamily: "InterD", fontSize: 22, fontWeight: 600, letterSpacing: "-0.02em" }}>What would you like to change?</div>
        <div style={{ fontSize: 14, color: C.ink2, margin: "6px 0 14px" }}>We’ll start a new search with these settings</div>
        {[["Wishes for the task", "Not specified"], ["Price per hour", "From 2,200 ₽"], ["Tutor", "Any gender"], ["Where to study", "Online"]].map(([a, b]) => (
          <div key={a} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "13px 0", borderBottom: `1px solid ${C.line}` }}>
            <div><div style={{ fontSize: 12.5, color: C.ink2 }}>{a}</div><div style={{ fontSize: 15.5, marginTop: 2 }}>{b}</div></div>
            <svg width={16} height={16} viewBox="0 0 24 24"><path d="M9 6l6 6-6 6" fill="none" stroke={C.hint} strokeWidth={2.2} strokeLinecap="round" /></svg>
          </div>
        ))}
        <Btn t="Find other pros" />
      </Sheet>
    }
  >
    <div style={{ padding: "18px 20px" }}>
      <Head t="Best fit for your task" s="Top by experience and reviews" />
      {ROWS.slice(0, 2).map((r, i) => <ListRow key={r.name} r={r} m praise={PRAISE[i]} />)}
    </div>
  </Phone>
);

const mob3 = (
  <Phone
    bg={C.bg}
    overlay={
      <Sheet>
        <div style={{ fontFamily: "InterD", fontSize: 22, fontWeight: 600, letterSpacing: "-0.02em" }}>Find other pros</div>
        <div style={{ fontSize: 14, color: C.ink2, margin: "6px 0 14px", lineHeight: "19px" }}>We filled this in from your order. Change anything and AI will pick three new specialists.</div>
        <div style={{ border: "1.5px solid #e3e5ee", borderRadius: 16, padding: "13px 15px", fontSize: 15, lineHeight: "22px", minHeight: 120 }}>
          Biology exam next week. Looking for a very experienced tutor, online, weekday evenings, up to 2,500 ₽ per hour
          <span style={{ display: "inline-block", width: 1.5, height: 18, background: C.ink, marginLeft: 2, verticalAlign: "-3px" }} />
        </div>
        <Btn t="Find other pros" />
      </Sheet>
    }
  >
    <div style={{ padding: "14px 12px" }}>
      <div style={{ padding: "4px 8px 12px" }}><Head t="Best for your task" s="Matched by experience and reviews" ai /></div>
      <LlmCard r={ROWS[0]} why={WHY3[0]} m />
      <LlmCard r={ROWS[1]} why={WHY3[1]} m />
    </div>
  </Phone>
);

const T4: Tutor = SET1[0];
const mob4 = (
  <Phone bg={C.bg}>
    <div style={{ padding: "14px 12px" }}>
      <div style={{ padding: "4px 8px 12px" }}><Head t="Best fit for your task" s="Picked by AI from 12 offers" ai /></div>
      {SET1.slice(0, 2).map((t, i) => (
        <div key={t.id} style={{ background: "#fff", borderRadius: 22, padding: 18, marginBottom: 10 }}>
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <Avatar img={t.img} size={48} online />
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 15, fontWeight: 600 }}>{t.name}<span style={{ display: "inline-flex", gap: 3, alignItems: "center", fontWeight: 400, fontSize: 13, color: C.ink2 }}><Star />{t.rating}</span></div>
              <div style={{ fontFamily: "InterD", fontSize: 21, fontWeight: 600, letterSpacing: "-0.02em" }}>{t.price} ₽ <span style={{ fontFamily: "Inter", fontSize: 13, fontWeight: 400, color: C.ink2 }}>per hour</span></div>
            </div>
          </div>
          <div style={{ marginTop: 12 }}><Why t={t} open={i === 0 ? 1 : 0} compact /></div>
          <div style={{ fontSize: 14, marginTop: 12 }}>{t.msg}</div>
        </div>
      ))}
    </div>
  </Phone>
);
void T4; void Check;

const DESK = [desk1, desk2, desk3, desk4];
const MOB = [mob1, mob2, mob3, mob4];
export const StageStill: React.FC<{ stage: number; kind: "d" | "m" }> = ({ stage, kind }) => (
  <AbsoluteFill style={{ background: "transparent" }}>
    <style>{fontCss}</style>
    {(kind === "d" ? DESK : MOB)[stage - 1]}
  </AbsoluteFill>
);
