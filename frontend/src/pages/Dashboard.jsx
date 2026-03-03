/**
 * Dashboard – main page layout that orchestrates all components.
 *
 * Layout:
 *  ┌──────────────┬─────────────────────────────────────┐
 *  │  Left Panel  │         Right Panel                  │
 *  │  - Input     │  - Gantt Chart                       │
 *  │  - Algorithm │  - Simulation Controls               │
 *  │  - Controls  │  - Process States                    │
 *  │              │                                      │
 *  ├──────────────┴─────────────────────────────────────┤
 *  │  Bottom Section                                     │
 *  │  - Metrics Table  │  - Comparison Charts            │
 *  └───────────────────┴────────────────────────────────┘
 */

import React, { useState, useCallback } from 'react';
import ProcessInput from '../components/ProcessInput';
import GanttChart from '../components/GanttChart';
import SimulationControls from '../components/SimulationControls';
import MetricsTable from '../components/MetricsTable';
import ComparisonChart from '../components/ComparisonChart';
import ProcessStateTimeline from '../components/ProcessStateTimeline';
import AlgorithmInfoPanel from '../components/AlgorithmInfo';
import useSimulation from '../hooks/useSimulation';
import { scheduleProcesses, compareAlgorithms, exportCSV, exportCompareCSV } from '../services/api';
import { downloadBlob, friendlyError } from '../utils/helpers';

export default function Dashboard() {
  // ─── State ──────────────────────────────────────────────────────
  const [processes, setProcesses] = useState([
    { pid: 'P1', arrival_time: 0, burst_time: 5, priority: 2 },
    { pid: 'P2', arrival_time: 1, burst_time: 3, priority: 1 },
    { pid: 'P3', arrival_time: 2, burst_time: 8, priority: 3 },
    { pid: 'P4', arrival_time: 3, burst_time: 2, priority: 4 },
  ]);
  const [algorithm, setAlgorithm] = useState('fcfs');
  const [timeQuantum, setTimeQuantum] = useState(2);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Results
  const [result, setResult] = useState(null);        // ScheduleResponse
  const [comparison, setComparison] = useState(null); // CompareResponse

  // Simulation hook
  const simulation = useSimulation(result?.gantt_chart || []);

  // ─── Run single algorithm ───────────────────────────────────────
  const handleRun = useCallback(async () => {
    setLoading(true);
    setError(null);
    setComparison(null);
    try {
      const payload = { processes, algorithm, time_quantum: timeQuantum };
      const data = await scheduleProcesses(payload);
      setResult(data);
    } catch (err) {
      setError(friendlyError(err));
      setResult(null);
    } finally {
      setLoading(false);
    }
  }, [processes, algorithm, timeQuantum]);

  // ─── Compare all algorithms ─────────────────────────────────────
  const handleCompare = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const payload = { processes, time_quantum: timeQuantum };
      const data = await compareAlgorithms(payload);
      setComparison(data.results);
      // Also set the first result as the active one
      const first = Object.values(data.results)[0];
      if (first) setResult(first);
    } catch (err) {
      setError(friendlyError(err));
    } finally {
      setLoading(false);
    }
  }, [processes, timeQuantum]);

  // ─── Export CSV ─────────────────────────────────────────────────
  const handleExportCSV = useCallback(async () => {
    try {
      if (comparison) {
        const blob = await exportCompareCSV({ processes, time_quantum: timeQuantum });
        downloadBlob(blob, 'comparison_results.csv');
      } else {
        const blob = await exportCSV({ processes, algorithm, time_quantum: timeQuantum });
        downloadBlob(blob, 'schedule_result.csv');
      }
    } catch {
      // Silently fail if export not available
    }
  }, [comparison, processes, algorithm, timeQuantum]);

  return (
    <div className="max-w-[1600px] mx-auto px-4 sm:px-6 py-6">
      {/* Error banner */}
      {error && (
        <div className="mb-4 p-3 rounded-lg bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 text-sm">
          ⚠ {error}
          <button onClick={() => setError(null)} className="ml-2 underline text-xs">Dismiss</button>
        </div>
      )}

      {/* ── Main two-column layout ──────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-[340px_1fr] gap-5">
        {/* LEFT PANEL */}
        <div className="space-y-4">
          <ProcessInput
            processes={processes}
            setProcesses={setProcesses}
            algorithm={algorithm}
            setAlgorithm={setAlgorithm}
            timeQuantum={timeQuantum}
            setTimeQuantum={setTimeQuantum}
            onRun={handleRun}
            onCompare={handleCompare}
            loading={loading}
          />
          <AlgorithmInfoPanel algorithm={algorithm} />
        </div>

        {/* RIGHT PANEL */}
        <div className="space-y-4">
          <GanttChart
            ganttChart={result?.gantt_chart || []}
            currentStep={simulation.currentStep}
          />

          <SimulationControls
            {...simulation}
            disabled={!result || result.gantt_chart.length === 0}
          />

          <ProcessStateTimeline
            ganttChart={result?.gantt_chart || []}
            processes={processes}
            currentStep={simulation.currentStep}
          />
        </div>
      </div>

      {/* ── Bottom section ──────────────────────────────────────── */}
      <div className="mt-6 grid grid-cols-1 xl:grid-cols-2 gap-5">
        <div className="space-y-4">
          <MetricsTable
            metrics={result?.metrics || null}
            algorithmName={result?.algorithm}
          />
          {/* Export button */}
          {result && (
            <button onClick={handleExportCSV} className="btn-secondary text-xs w-full">
              📥 Export Results as CSV
            </button>
          )}
        </div>
        <ComparisonChart comparisonResults={comparison} />
      </div>
    </div>
  );
}
