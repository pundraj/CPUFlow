/**
 * MetricsTable – displays per-process and summary scheduling metrics.
 *
 * Shows completion time, turnaround time, waiting time, and response time
 * for each process, plus aggregated averages, CPU utilization, and throughput.
 */

import React from 'react';
import { motion } from 'framer-motion';
import { getProcessColor } from '../utils/helpers';

export default function MetricsTable({ metrics, algorithmName }) {
  if (!metrics) {
    return (
      <div className="card p-6 flex items-center justify-center h-32">
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Metrics will appear after running an algorithm
        </p>
      </div>
    );
  }

  const pids = Object.keys(metrics.completion_times).sort((a, b) => {
    const na = parseInt(a.replace(/\D/g, ''), 10) || 0;
    const nb = parseInt(b.replace(/\D/g, ''), 10) || 0;
    return na - nb;
  });

  return (
    <div className="card p-4 overflow-hidden">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold">Performance Metrics</h3>
        {algorithmName && (
          <span className="text-[11px] px-2 py-0.5 rounded-full bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 font-medium">
            {algorithmName}
          </span>
        )}
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
        {[
          { label: 'Avg Waiting Time', value: metrics.average_waiting_time, unit: '' },
          { label: 'Avg Turnaround', value: metrics.average_turnaround_time, unit: '' },
          { label: 'CPU Utilization', value: metrics.cpu_utilization, unit: '%' },
          { label: 'Throughput', value: metrics.throughput, unit: ' p/u' },
        ].map((m) => (
          <motion.div
            key={m.label}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-3 rounded-lg"
            style={{ backgroundColor: 'var(--bg-primary)' }}
          >
            <div className="text-[10px] uppercase tracking-wider mb-1" style={{ color: 'var(--text-secondary)' }}>
              {m.label}
            </div>
            <div className="text-lg font-bold">
              {m.value}{m.unit}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Per-process table */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="text-left" style={{ color: 'var(--text-secondary)' }}>
              <th className="pb-2 font-semibold">PID</th>
              <th className="pb-2 font-semibold text-center">Completion</th>
              <th className="pb-2 font-semibold text-center">Turnaround</th>
              <th className="pb-2 font-semibold text-center">Waiting</th>
              <th className="pb-2 font-semibold text-center">Response</th>
            </tr>
          </thead>
          <tbody>
            {pids.map((pid) => (
              <motion.tr
                key={pid}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="border-t"
                style={{ borderColor: 'var(--border-color)' }}
              >
                <td className="py-2 font-medium flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: getProcessColor(pid) }} />
                  {pid}
                </td>
                <td className="py-2 text-center font-mono">{metrics.completion_times[pid]}</td>
                <td className="py-2 text-center font-mono">{metrics.turnaround_times[pid]}</td>
                <td className="py-2 text-center font-mono">{metrics.waiting_times[pid]}</td>
                <td className="py-2 text-center font-mono">{metrics.response_times[pid]}</td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
