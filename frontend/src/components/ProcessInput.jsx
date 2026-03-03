/**
 * ProcessInput – form panel for adding, removing, and configuring processes.
 *
 * Features:
 *  - Dynamic process addition / removal
 *  - Algorithm selection dropdown
 *  - Time quantum input (for RR / MLFQ)
 *  - Random process generator
 *  - Reset button
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ALGORITHM_LABELS, generateRandomProcesses } from '../utils/helpers';

const ALGORITHMS = Object.entries(ALGORITHM_LABELS);
const NEEDS_PRIORITY = ['priority_np', 'priority_p', 'multilevel_queue'];
const NEEDS_QUANTUM = ['round_robin', 'mlfq'];

export default function ProcessInput({
  processes,
  setProcesses,
  algorithm,
  setAlgorithm,
  timeQuantum,
  setTimeQuantum,
  onRun,
  onCompare,
  loading,
}) {
  // ─── Add a blank process row ───────────────────────────────────────
  const addProcess = () => {
    const nextId = processes.length > 0
      ? Math.max(...processes.map((p) => parseInt(p.pid.replace('P', ''), 10) || 0)) + 1
      : 1;
    setProcesses([
      ...processes,
      { pid: `P${nextId}`, arrival_time: 0, burst_time: 1, priority: 0 },
    ]);
  };

  // ─── Remove a process by index ─────────────────────────────────────
  const removeProcess = (idx) => {
    setProcesses(processes.filter((_, i) => i !== idx));
  };

  // ─── Update a field in a process ───────────────────────────────────
  const updateProcess = (idx, field, value) => {
    const updated = [...processes];
    updated[idx] = { ...updated[idx], [field]: field === 'pid' ? value : Math.max(0, Number(value) || 0) };
    setProcesses(updated);
  };

  // ─── Random fill ───────────────────────────────────────────────────
  const generateRandom = () => {
    setProcesses(generateRandomProcesses(5));
  };

  // ─── Reset ─────────────────────────────────────────────────────────
  const reset = () => {
    setProcesses([{ pid: 'P1', arrival_time: 0, burst_time: 1, priority: 0 }]);
  };

  const showPriority = NEEDS_PRIORITY.includes(algorithm) || algorithm === 'mlfq';
  const showQuantum = NEEDS_QUANTUM.includes(algorithm);

  return (
    <div className="card p-5 space-y-5">
      {/* ── Algorithm selector ────────────────────────────────────── */}
      <div>
        <label className="label">Scheduling Algorithm</label>
        <select
          className="input-field"
          value={algorithm}
          onChange={(e) => setAlgorithm(e.target.value)}
        >
          {ALGORITHMS.map(([key, label]) => (
            <option key={key} value={key}>{label}</option>
          ))}
        </select>
      </div>

      {/* ── Time quantum (conditional) ────────────────────────────── */}
      {showQuantum && (
        <div>
          <label className="label">Time Quantum</label>
          <input
            type="number"
            className="input-field"
            min={1}
            value={timeQuantum}
            onChange={(e) => setTimeQuantum(Math.max(1, Number(e.target.value) || 1))}
          />
        </div>
      )}

      {/* ── Process table ─────────────────────────────────────────── */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <span className="label mb-0">Processes</span>
          <span className="text-xs" style={{ color: 'var(--text-secondary)' }}>
            {processes.length} process{processes.length !== 1 && 'es'}
          </span>
        </div>

        {/* Header row */}
        <div className={`grid gap-2 text-[11px] font-semibold uppercase tracking-wider mb-1 ${showPriority ? 'grid-cols-[60px_1fr_1fr_1fr_32px]' : 'grid-cols-[60px_1fr_1fr_32px]'}`}
          style={{ color: 'var(--text-secondary)' }}>
          <span>PID</span>
          <span>Arrival</span>
          <span>Burst</span>
          {showPriority && <span>Priority</span>}
          <span></span>
        </div>

        {/* Process rows */}
        <AnimatePresence>
          {processes.map((proc, idx) => (
            <motion.div
              key={proc.pid + idx}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.15 }}
              className={`grid gap-2 mb-1.5 ${showPriority ? 'grid-cols-[60px_1fr_1fr_1fr_32px]' : 'grid-cols-[60px_1fr_1fr_32px]'}`}
            >
              <input
                className="input-field text-center font-mono text-xs"
                value={proc.pid}
                onChange={(e) => updateProcess(idx, 'pid', e.target.value)}
              />
              <input
                type="number"
                className="input-field text-center text-xs"
                min={0} value={proc.arrival_time}
                onChange={(e) => updateProcess(idx, 'arrival_time', e.target.value)}
              />
              <input
                type="number"
                className="input-field text-center text-xs"
                min={0} value={proc.burst_time}
                onChange={(e) => updateProcess(idx, 'burst_time', e.target.value)}
              />
              {showPriority && (
                <input
                  type="number"
                  className="input-field text-center text-xs"
                  min={0} value={proc.priority}
                  onChange={(e) => updateProcess(idx, 'priority', e.target.value)}
                />
              )}
              <button
                onClick={() => removeProcess(idx)}
                className="flex items-center justify-center text-red-400 hover:text-red-600 transition-colors"
                title="Remove process"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Add process button */}
        <button onClick={addProcess} className="w-full mt-2 py-1.5 rounded-lg border border-dashed text-xs font-medium transition-colors hover:border-primary-400 hover:text-primary-500"
          style={{ borderColor: 'var(--border-color)', color: 'var(--text-secondary)' }}>
          + Add Process
        </button>
      </div>

      {/* ── Action buttons ────────────────────────────────────────── */}
      <div className="space-y-2">
        <button onClick={onRun} disabled={loading || processes.length === 0} className="btn-primary w-full">
          {loading ? 'Scheduling…' : '▶ Run Algorithm'}
        </button>
        <button onClick={onCompare} disabled={loading || processes.length === 0} className="btn-secondary w-full text-sm">
          📊 Compare All Algorithms
        </button>
        <div className="flex gap-2">
          <button onClick={generateRandom} className="btn-secondary flex-1 text-xs">
            🎲 Random
          </button>
          <button onClick={reset} className="btn-secondary flex-1 text-xs">
            ↺ Reset
          </button>
        </div>
      </div>
    </div>
  );
}
