import { Composition } from "remotion";
import { CaseClip, Cover, COVER_SECONDS, FPS } from "./Cover";
import { AbsoluteFill } from "remotion";
import { Mobile } from "./ui/Mobile";
import { MobileClip } from "./MobileClip";
import { PhoneSplash } from "./PhoneSplash";
import { fontCss } from "./theme";
import { StageStill } from "./Stages";
import { Still } from "remotion";

const PhoneStill: React.FC = () => (
  <AbsoluteFill>
    <style>{fontCss}</style>
    <div style={{ transformOrigin: "0 0", scale: "2" }}>
      <Mobile open={0} height={730} scroll={0} />
    </div>
  </AbsoluteFill>
);

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="ProfiCover" component={Cover} durationInFrames={Math.round(COVER_SECONDS * FPS)} fps={FPS} width={1440} height={900} />
      <Composition id="ProfiMatch" component={CaseClip} defaultProps={{ intro: true }} durationInFrames={Math.round(4.2 * FPS)} fps={FPS} width={2000} height={1196} />
      <Composition id="ProfiRepick" component={CaseClip} defaultProps={{ intro: false }} durationInFrames={Math.round(14.6 * FPS)} fps={FPS} width={2000} height={1196} />
      <Composition id="ProfiMobile" component={MobileClip} durationInFrames={Math.round(8.4 * FPS)} fps={FPS} width={2000} height={1196} />
      <Composition id="PhoneSplash" component={PhoneSplash} durationInFrames={40} fps={25} width={412} height={730} />
      <Still id="S1d" component={StageStill} width={1366} height={800} defaultProps={{ stage: 1, kind: "d" as const }} />
      <Still id="S1m" component={StageStill} width={393} height={852} defaultProps={{ stage: 1, kind: "m" as const }} />
      <Still id="S2d" component={StageStill} width={1366} height={800} defaultProps={{ stage: 2, kind: "d" as const }} />
      <Still id="S2m" component={StageStill} width={393} height={852} defaultProps={{ stage: 2, kind: "m" as const }} />
      <Still id="S3d" component={StageStill} width={1366} height={800} defaultProps={{ stage: 3, kind: "d" as const }} />
      <Still id="S3m" component={StageStill} width={393} height={852} defaultProps={{ stage: 3, kind: "m" as const }} />
      <Still id="S4d" component={StageStill} width={1366} height={800} defaultProps={{ stage: 4, kind: "d" as const }} />
      <Still id="S4m" component={StageStill} width={393} height={852} defaultProps={{ stage: 4, kind: "m" as const }} />
      <Composition id="PhoneStill" component={PhoneStill} durationInFrames={1} fps={FPS} width={824} height={1460} />
    </>
  );
};
