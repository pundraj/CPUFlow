/**
 * SimulationControls – playback controls for step-by-step simulation.
 *
 * Play / Pause / Stop / Step Forward / Step Backward / Jump to End
 * Speed selector: Slow, Medium, Fast
 */

import React from 'react';
import { SPEED_PRESETS } from '../utils/helpers';

export default function SimulationControls({
  isPlaying,
  play,
  pause,
  stop,
  stepForward,
  stepBackward,
  jumpToEnd,
  speed,
  setSpeed,
  currentStep,
  totalSteps,
  disabled,
}) {
  const speeds = Object.keys(SPEED_PRESETS);

  return (
    <div className="card p-3 flex flex-wrap items-center gap-3">
      {/* Playback buttons */}
      <div className="flex items-center gap-1">
        <button
          onClick={stepBackward}
          disabled={disabled || currentStep <= 0}
          className="btn-secondary !px-2 !py-1.5 text-xs"
          title="Step backward"
        >
          ⏮
        </button>
        {isPlaying ? (
          <button onClick={pause} disabled={disabled} className="btn-primary !px-3 !py-1.5 text-xs" title="Pause">
            ⏸
          </button>
        ) : (
          <button onClick={play} disabled={disabled || totalSteps === 0} className="btn-primary !px-3 !py-1.5 text-xs" title="Play">
            ▶
          </button>
        )}
        <button
          onClick={stepForward}
          disabled={disabled || currentStep >= totalSteps - 1}
          className="btn-secondary !px-2 !py-1.5 text-xs"
          title="Step forward"
        >
          ⏭
        </button>
        <button onClick={stop} disabled={disabled} className="btn-secondary !px-2 !py-1.5 text-xs" title="Stop">
          ⏹
        </button>
        <button onClick={jumpToEnd} disabled={disabled || totalSteps === 0} className="btn-secondary !px-2 !py-1.5 text-xs" title="Jump to end">
          ⏩
        </button>
      </div>

      {/* Progress indicator */}
      <div className="text-xs font-mono" style={{ color: 'var(--text-secondary)' }}>
        Step {Math.max(currentStep + 1, 0)} / {totalSteps}
      </div>

      {/* Speed selector */}
      <div className="flex items-center gap-1 ml-auto">
        <span className="text-[11px]" style={{ color: 'var(--text-secondary)' }}>Speed:</span>
        {speeds.map((s) => (
          <button
            key={s}
            onClick={() => setSpeed(s)}
            className={`px-2 py-1 rounded text-[11px] font-medium transition-colors
              ${speed === s
                ? 'bg-primary-600 text-white'
                : 'hover:bg-gray-200 dark:hover:bg-gray-700'
              }`}
            style={speed !== s ? { color: 'var(--text-secondary)' } : {}}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
