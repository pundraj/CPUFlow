/**
 * ProcessStateTimeline – shows the state transitions of each process.
 * Ready → Running → Completed (with animated indicators)
 */

import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { getProcessColor } from '../utils/helpers';

export default function ProcessStateTimeline({ ganttChart = [], processes = [], currentStep = -1 }) {
  // Determine the state of each process at the current point in the animation
  const processStates = useMemo(() => {
    if (!ganttChart.length || !processes.length) return {};

    const visibleEntries = currentStep < 0 ? ganttChart : ganttChart.slice(0, currentStep + 1);
    const currentTime = visibleEntries.length > 0
      ? visibleEntries[visibleEntries.length - 1].end
      : 0;

    const states = {};
    for (const proc of processes) {
      const pid = proc.pid;

      // Check if process is completed
      const allEntries = visibleEntries.filter((e) => e.process === pid);
      const totalRan = allEntries.reduce((sum, e) => sum + (e.end - e.start), 0);

      if (totalRan >= proc.burst_time && proc.burst_time > 0) {
        states[pid] = 'Completed';
      } else if (visibleEntries.length > 0 && visibleEntries[visibleEntries.length - 1].process === pid) {
        states[pid] = 'Running';
      } else if (proc.arrival_time <= currentTime && proc.burst_time > 0) {
        states[pid] = 'Ready';
      } else if (proc.burst_time === 0) {
        states[pid] = 'Completed';
      } else {
        states[pid] = 'Not Arrived';
      }
    }
    return states;
  }, [ganttChart, processes, currentStep]);

  if (processes.length === 0) return null;

  const stateColors = {
    'Not Arrived': '#94a3b8',
    Ready: '#f59e0b',
    Running: '#10b981',
    Completed: '#3b82f6',
  };

  return (
    <div className="card p-4">
      <h3 className="text-sm font-semibold mb-3">Process States</h3>
      <div className="flex flex-wrap gap-2">
        {processes.map((proc) => {
          const state = processStates[proc.pid] || 'Not Arrived';
          return (
            <motion.div
              key={proc.pid}
              layout
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium"
              style={{ backgroundColor: 'var(--bg-primary)' }}
            >
              <div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: getProcessColor(proc.pid) }}
              />
              <span>{proc.pid}</span>
              <span
                className="px-1.5 py-0.5 rounded text-[10px] font-bold text-white"
                style={{ backgroundColor: stateColors[state] }}
              >
                {state}
              </span>
            </motion.div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="flex gap-4 mt-3 pt-2 border-t" style={{ borderColor: 'var(--border-color)' }}>
        {Object.entries(stateColors).map(([label, color]) => (
          <div key={label} className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
            <span className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
