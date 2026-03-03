/**
 * Custom hook that manages the scheduling simulation state.
 *
 * Provides step-by-step playback, speed control, and animation state
 * for the Gantt chart visualization.
 */

import { useState, useRef, useCallback, useEffect } from 'react';
import { SPEED_PRESETS } from '../utils/helpers';

export default function useSimulation(ganttChart = []) {
  const [currentStep, setCurrentStep] = useState(-1); // -1 = not started
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState('Medium');
  const intervalRef = useRef(null);

  const totalSteps = ganttChart.length;

  // Clean up interval on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  // Reset when gantt chart changes
  useEffect(() => {
    stop();
    setCurrentStep(-1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ganttChart]);

  const play = useCallback(() => {
    if (totalSteps === 0) return;
    setIsPlaying(true);

    const ms = SPEED_PRESETS[speed] || 500;
    let step = currentStep < 0 ? -1 : currentStep;

    // Show the first step immediately so step 0 is not skipped
    if (step < 0) {
      step = 0;
      setCurrentStep(0);
    }

    intervalRef.current = setInterval(() => {
      if (step >= totalSteps - 1) {
        clearInterval(intervalRef.current);
        setIsPlaying(false);
        setCurrentStep(totalSteps - 1);
        return;
      }
      step++;
      setCurrentStep(step);
    }, ms);
  }, [currentStep, speed, totalSteps]);

  const pause = useCallback(() => {
    setIsPlaying(false);
    if (intervalRef.current) clearInterval(intervalRef.current);
  }, []);

  const stop = useCallback(() => {
    setIsPlaying(false);
    if (intervalRef.current) clearInterval(intervalRef.current);
    setCurrentStep(-1);
  }, []);

  const stepForward = useCallback(() => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep((s) => s + 1);
    }
  }, [currentStep, totalSteps]);

  const stepBackward = useCallback(() => {
    if (currentStep > 0) {
      setCurrentStep((s) => s - 1);
    }
  }, [currentStep]);

  const jumpToEnd = useCallback(() => {
    setCurrentStep(totalSteps - 1);
    pause();
  }, [totalSteps, pause]);

  return {
    currentStep,
    isPlaying,
    speed,
    setSpeed,
    play,
    pause,
    stop,
    stepForward,
    stepBackward,
    jumpToEnd,
    totalSteps,
    isComplete: currentStep >= totalSteps - 1,
  };
}
