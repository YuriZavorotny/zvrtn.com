import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, interpolate, Easing} from 'remotion';

// Все координаты в пикселях кадра 2000x1248 (сняты с ab.html через getBoundingClientRect).
const FPS = 30;
const s = (sec: number) => Math.round(sec * FPS);
export const DURATION = s(21);
const ease = Easing.bezier(0.45, 0, 0.2, 1);
const out = Easing.bezier(0.16, 1, 0.3, 1);
const cl = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// таймлайн (сек)
const T = {
  openGen: 2.6,      // клик «Generate with Sweed AI»
  focusTa: 3.9,      // клик в поле запроса
  type1: [4.1, 5.9], type2: [5.9, 7.0],
  genClick: 8.1,     // клик «Generate drafts»
  skel: [8.25, 9.6],
  cards: [9.6, 10.0, 10.4],
  addClick: 12.9,    // клик «Add 2 variants»
  startClick: 15.6,  // клик «Start test»
  loop: [20.3, 21],  // возврат к первому кадру для бесшовного цикла
};
// путь курсора: [сек, x, y]
const PATH: [number, number, number][] = [
  [0, 1150, 820], [1.0, 1150, 820], [2.1, 1612, 742],
  [3.0, 1612, 742], [3.7, 1560, 452],
  [7.1, 1560, 452], [7.9, 1300, 1188],
  [10.8, 1300, 1188], [11.5, 1700, 1070], [12.1, 1700, 1070], [12.7, 1300, 1188],
  [13.8, 1300, 1188], [15.3, 1445, 1188],
  [16.4, 1445, 1188], [17.4, 1530, 978], [21, 1530, 978],
];
const CLICKS = [T.openGen, T.focusTa, T.genClick, T.addClick, T.startClick];

const img = (n: string) => staticFile(`s${n}.png`);
const Layer: React.FC<{n: string; o: number}> = ({n, o}) => o <= 0 ? null : (
  <Img src={img(n)} style={{position: 'absolute', left: 0, top: 0, width: 2000, height: 1249, opacity: o}} />
);
// кусок другого кадра в тех же координатах
const Crop: React.FC<{n: string; r: number[]; o: number; dy?: number}> = ({n, r, o, dy = 0}) => o <= 0 ? null : (
  <div style={{position: 'absolute', left: r[0], top: r[1], width: r[2], height: r[3], overflow: 'hidden', opacity: o, translate: `0 ${dy}px`}}>
    <Img src={img(n)} style={{position: 'absolute', left: -r[0], top: -r[1], width: 2000, height: 1249}} />
  </div>
);

const fade = (f: number, at: number, dur = 0.35) => interpolate(f, [s(at), s(at + dur)], [0, 1], {...cl, easing: ease});

const Cursor: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  let x = PATH[0][1], y = PATH[0][2];
  for (let i = 0; i < PATH.length - 1; i++) {
    const [t0, x0, y0] = PATH[i], [t1, x1, y1] = PATH[i + 1];
    if (t >= t0 && t <= t1) {
      const k = t1 === t0 ? 1 : ease((t - t0) / (t1 - t0));
      x = x0 + (x1 - x0) * k; y = y0 + (y1 - y0) * k; break;
    }
    if (t > t1) { x = x1; y = y1; }
  }
  const press = CLICKS.reduce((m, c) => Math.max(m, interpolate(f, [s(c) - 3, s(c), s(c) + 5], [0, 1, 0], cl)), 0);
  const fadeOut = interpolate(f, [s(T.loop[0]), s(T.loop[0] + 0.3)], [1, 0], cl);
  return (
    <>
      {CLICKS.map((c) => {
        const p = interpolate(f, [s(c), s(c) + 16], [0, 1], cl);
        if (p <= 0 || p >= 1) return null;
        return <div key={c} style={{position: 'absolute', left: x - 34, top: y - 34, width: 68, height: 68, borderRadius: '50%',
          background: 'rgba(18,19,15,.18)', scale: String(0.3 + p * 1.1), opacity: 1 - out(p)}} />;
      })}
      <svg width="34" height="34" viewBox="0 0 24 24" style={{position: 'absolute', left: x - 5, top: y - 3, scale: String(1 - press * 0.12), opacity: fadeOut,
        filter: 'drop-shadow(0 2px 3px rgba(0,0,0,.25))'}}>
        <path d="M5 2.5l13.5 12.2-6.1.6 3.6 7.2-2.7 1.3-3.5-7.3-4.8 4.2z" fill="#12130f" stroke="#fff" strokeWidth="1.4" strokeLinejoin="round" />
      </svg>
    </>
  );
};

// набор текста: построчная «шторка» по кадру sf + каретка
const LINES = [[1384.7, 423.6, 497.2, 20.8], [1384.7, 448.6, 359.9, 20.8]];
const Typing: React.FC = () => {
  const f = useCurrentFrame();
  if (f < s(T.focusTa) || f >= s(T.type2[1]) + 6) return null;
  const w1 = interpolate(f, [s(T.type1[0]), s(T.type1[1])], [0, 1], cl);
  const w2 = interpolate(f, [s(T.type2[0]), s(T.type2[1])], [0, 1], cl);
  // ступенчато, как печать по символам
  const step = (w: number, n: number) => Math.round(w * n) / n;
  const p1 = step(w1, 62), p2 = step(w2, 44);
  const [l1, l2] = LINES;
  const onL2 = f >= s(T.type2[0]);
  const cx = onL2 ? l2[0] + l2[2] * p2 : l1[0] + l1[2] * p1;
  const cy = onL2 ? l2[1] : l1[1];
  const blink = (f >= s(T.type1[0]) && f < s(T.type2[1])) ? 1 : (Math.floor(f / 15) % 2 ? 0 : 1);
  return (
    <>
      <Crop n="f" r={[l1[0] - 2, l1[1] - 2, l1[2] * p1 + 2, l1[3] + 4]} o={p1 > 0 ? 1 : 0} />
      <Crop n="f" r={[l2[0] - 2, l2[1] - 2, l2[2] * p2 + 2, l2[3] + 4]} o={p2 > 0 ? 1 : 0} />
      <div style={{position: 'absolute', left: cx + 1, top: cy, width: 2, height: 22, background: '#a682ff', opacity: blink}} />
    </>
  );
};

const DC = [[1367, 663, 543, 142], [1367, 821, 543, 119], [1367, 957, 543, 142]];
const DH = [1367, 612, 543, 40];
const Skeleton: React.FC = () => {
  const f = useCurrentFrame();
  const o = interpolate(f, [s(T.skel[0]), s(T.skel[0]) + 6, s(T.skel[1]), s(T.skel[1]) + 8], [0, 1, 1, 0], cl);
  if (o <= 0) return null;
  const sh = ((f - s(T.skel[0])) % 36) / 36; // бегущий блик
  return (
    <>
      {DC.map((r, i) => (
        <div key={i} style={{position: 'absolute', left: r[0], top: r[1], width: r[2], height: r[3], borderRadius: 11, opacity: o,
          border: '1.4px solid #e8e8e7', overflow: 'hidden', background: '#fff'}}>
          {[0.62, 0.86, 0.38].map((w, j) => (
            <div key={j} style={{position: 'absolute', left: 50, top: 22 + j * 30, width: (r[2] - 80) * w, height: 14, borderRadius: 7, background: 'rgba(166,130,255,.16)'}} />
          ))}
          <div style={{position: 'absolute', top: 0, bottom: 0, width: 220, left: -220 + sh * (r[2] + 440),
            background: 'linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.75), rgba(255,255,255,0))'}} />
        </div>
      ))}
    </>
  );
};

// мягкая подсветка новых AI-строк в таблице после добавления
const ROWS = [[1367, 1003, 543, 63], [1367, 1065, 543, 63]];
const RowFlash: React.FC = () => {
  const f = useCurrentFrame();
  const o = interpolate(f, [s(T.addClick + 0.4), s(T.addClick + 0.8), s(T.addClick + 2.2), s(T.addClick + 3)], [0, 1, 1, 0], cl);
  if (o <= 0) return null;
  return <>{ROWS.map((r, i) => <div key={i} style={{position: 'absolute', left: r[0], top: r[1], width: r[2], height: r[3], background: 'rgba(166,130,255,.10)', opacity: o}} />)}</>;
};

export const SweedAI: React.FC = () => {
  const f = useCurrentFrame();
  const oE = fade(f, T.openGen + 0.1);
  const oG = fade(f, T.genClick + 0.12, 0.3);
  const cards = T.cards.map((c) => interpolate(f, [s(c), s(c + 0.45)], [0, 1], {...cl, easing: out}));
  const o1 = fade(f, T.addClick + 0.15);
  const o3 = fade(f, T.startClick + 0.15);
  const oLoop = fade(f, T.loop[0], 0.6);
  // лёгкий наезд камеры на панель, пока идёт работа с AI
  const zoom = interpolate(f, [s(T.openGen), s(T.openGen + 1.4), s(T.addClick - 0.2), s(T.addClick + 1.2)], [1, 1.02, 1.02, 1], {...cl, easing: ease});
  return (
    <AbsoluteFill style={{background: '#fff', overflow: 'hidden'}}>
      <AbsoluteFill style={{scale: String(zoom), transformOrigin: '1640px 660px'}}>
        <Layer n="0" o={1} />
        <Layer n="e" o={oE} />
        <Typing />
        <Layer n="f" o={f >= s(T.type2[1]) + 6 ? 1 : 0} />
        <Layer n="g" o={oG} />
        <Skeleton />
        {f >= s(T.cards[0]) && <Crop n="2" r={DH} o={cards[0]} />}
        {DC.map((r, i) => <Crop key={i} n="2" r={r} o={cards[i]} dy={(1 - cards[i]) * 14} />)}
        <Layer n="1" o={o1} />
        <RowFlash />
        <Layer n="3" o={o3} />
        <Layer n="0" o={oLoop} />
        <Cursor />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
