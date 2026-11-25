import React from 'react';
import {Composition} from 'remotion';
import {SweedAI, DURATION} from './SweedAI';
export const Root: React.FC = () => (
  <Composition id="SweedAI" component={SweedAI} width={2000} height={1248} fps={30} durationInFrames={DURATION} />
);
