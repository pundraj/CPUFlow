/**
 * GanttChart – animated timeline visualization of scheduling results.
 *
 * Features:
 *  - Color-coded process blocks
 *  - Animated reveal (step-by-step or all-at-once)
 *  - Responsive horizontal scrolling
 *  - Idle time visualization
 *  - Hover tooltips
 */

import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { getProcessColor } from '../utils/helpers';

const UNIT_WIDTH = 48; // pixels per time unit
const BAR_HEIGHT = 44;

export default function GanttChart({ ganttChart = [], currentStep = -1 }) {
  // Total timeline length
  const totalTime = useMemo(() => {
    if (ganttChart.length === 0) return 0;
    return Math.max(...ganttChart.map((e) => e.end));
  }, [ganttChart]);

  if (ganttChart.length === 0) {
    return (
      <div className="card p-6 flex items-center justify-center h-40">
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Run an algorithm to see the Gantt chart
        </p>
      </div>
    );
  }

  // Show all entries up to the current step (or all if -1 / complete)
  const visibleEntries =
    currentStep < 0
      ? ganttChart
      : ganttChart.slice(0, currentStep + 1);

  return (
    <div className="card p-4 overflow-hidden">
      <h3 className="text-sm font-semibold mb-3">Gantt Chart Timeline</h3>

      {/* Scrollable container */}
      <div className="overflow-x-auto pb-2" style={{ maxWidth: '100%' }}>
        <div style={{ minWidth: totalTime * UNIT_WIDTH + 40, position: 'relative' }}>
          {/* Time axis labels */}
          <div className="flex" style={{ marginBottom: 4, marginLeft: 0 }}>
            {Array.from({ length: totalTime + 1 }, (_, i) => (
              <div
                key={i}
                className="text-[10px] font-mono text-center flex-shrink-0"
                style={{ width: UNIT_WIDTH, color: 'var(--text-secondary)' }}
              >
                {i}
              </div>
            ))}
          </div>

          {/* Bars */}
          <div className="relative" style={{ height: BAR_HEIGHT + 8 }}>
            {visibleEntries.map((entry, idx) => {
              const width = (entry.end - entry.start) * UNIT_WIDTH;
              const left = entry.start * UNIT_WIDTH;
              const isIdle = entry.process === 'Idle';
              const color = getProcessColor(entry.process);

              return (
                <motion.div
                  key={`${entry.process}-${entry.start}-${idx}`}
                  initial={{ opacity: 0, scaleX: 0 }}
                  animate={{ opacity: 1, scaleX: 1 }}
                  transition={{ duration: 0.3, delay: idx * 0.05 }}
                  style={{
                    position: 'absolute',
                    left,
                    top: 4,
                    width,
                    height: BAR_HEIGHT,
                    backgroundColor: isIdle ? 'transparent' : color,
                    borderRadius: 8,
                    border: isIdle ? '2px dashed var(--border-color)' : `2px solid ${color}`,
                    transformOrigin: 'left center',
                  }}
                  className="flex items-center justify-center cursor-default group"
                  title={`${entry.process}: ${entry.start} → ${entry.end} (${entry.end - entry.start} units)`}
                >
                  <span
                    className="text-xs font-bold truncate px-1"
                    style={{ color: isIdle ? 'var(--text-secondary)' : '#fff' }}
                  >
                    {entry.process}
                  </span>

                  {/* Tooltip on hover */}
                  <div className="absolute -top-10 left-1/2 -translate-x-1/2 hidden group-hover:block z-10">
                    <div className="bg-gray-900 text-white text-[10px] rounded px-2 py-1 whitespace-nowrap shadow-lg">
                      {entry.process} | {entry.start}–{entry.end} ({entry.end - entry.start}u)
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-3 mt-3 pt-3 border-t" style={{ borderColor: 'var(--border-color)' }}>
        {[...new Set(ganttChart.map((e) => e.process))].map((pid) => (
          <div key={pid} className="flex items-center gap-1.5">
            <div
              className="w-3 h-3 rounded-sm"
              style={{
                backgroundColor: pid === 'Idle' ? 'transparent' : getProcessColor(pid),
                border: pid === 'Idle' ? '1.5px dashed var(--text-secondary)' : 'none',
              }}
            />
            <span className="text-[11px] font-medium" style={{ color: 'var(--text-secondary)' }}>
              {pid}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
