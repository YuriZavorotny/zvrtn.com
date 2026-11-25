import { staticFile } from "remotion";

export const C = {
  ink: "#181818",
  ink2: "#838398",
  hint: "#a9a9c1",
  bg: "#f3f4f8",
  ctl: "#eff1f8",
  line: "rgba(4,4,15,0.07)",
  brand: "#fa2a48",
  ai: "#fff4e0",
  aiInk: "#8a5a00",
  aiStar: "#f5a524",
  ok: "#1bb577",
  dark: "#2f3038",
};

export const fontCss = `
@font-face{font-family:Inter;font-weight:400;src:url(${staticFile("fonts/Inter-Regular.otf")})}
@font-face{font-family:Inter;font-weight:500;src:url(${staticFile("fonts/Inter-Medium.otf")})}
@font-face{font-family:Inter;font-weight:600;src:url(${staticFile("fonts/Inter-SemiBold.otf")})}
@font-face{font-family:InterD;font-weight:600;src:url(${staticFile("fonts/InterDisplay-SemiBold.otf")})}
@font-face{font-family:Mont;src:url(${staticFile("fonts/Montserrat.ttf")})}
`;

export type Tutor = {
  id: string;
  name: string;
  img: string;
  rating: string;
  reviews: number;
  price: string;
  why: string;
  crit: string[];
  src: string;
  msg: string;
  time: string;
};

export const SET1: Tutor[] = [
  { id: "a", name: "Olivia M.", img: "olivia", rating: "5.0", reviews: 54, price: "2,200", why: "Asks about your goal for the exam and where you get stuck, then builds lessons around the gaps.", crit: ["Within budget", "Weekday evenings", "Online"], src: "From 54 reviews: “explains the hardest topics step by step”", msg: "Happy to start with a short call to plan your prep", time: "07:20" },
  { id: "b", name: "Victoria B.", img: "victoria", rating: "4.8", reviews: 43, price: "2,100", why: "13 years preparing students for the biology exam, works through past papers in every lesson.", crit: ["Within budget", "Online"], src: "From 43 reviews: “clear plan from the first lesson”", msg: "Let’s set up a call to go through your task", time: "06:20" },
  { id: "c", name: "Anna F.", img: "anna", rating: "4.9", reviews: 133, price: "2,400", why: "Finds out what is hard for you before the first lesson and doesn’t push extra hours.", crit: ["Within budget", "Weekday evenings"], src: "From 133 reviews: “patient and well prepared”", msg: "Ready to meet and talk through your request", time: "05:20" },
];

export const SET2: Tutor[] = [
  { id: "d", name: "Kate A.", img: "kate", rating: "5.0", reviews: 45, price: "1,200", why: "Half your old budget and a strong exam record. Focuses on the question types that cost the most points.", crit: ["Up to 1,500 ₽", "Weekday evenings", "Online"], src: "From 45 reviews: “my score went up by 20 points”", msg: "Let’s organise a call to go over the details", time: "04:20" },
  { id: "e", name: "Helen T.", img: "helen", rating: "4.9", reviews: 432, price: "1,100", why: "10 years of exam prep in biology. Starts with a short test to see where to begin.", crit: ["Up to 1,500 ₽", "Online"], src: "From 432 reviews: “structured and calm”", msg: "Happy to meet and plan your lessons", time: "04:20" },
  { id: "f", name: "Irene G.", img: "irene", rating: "4.9", reviews: 453, price: "1,400", why: "Asks what you struggle with before lessons start, flexible with evening slots.", crit: ["Up to 1,500 ₽", "Weekday evenings"], src: "From 453 reviews: “always on time, clear homework”", msg: "Ready to discuss the details of your request", time: "04:20" },
];
