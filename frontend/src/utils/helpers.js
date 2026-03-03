/**
 * Utility functions shared across the frontend.
 */

// ─── Process color palette ───────────────────────────────────────────
const PROCESS_COLORS = [
  '#3b82f6', // blue
  '#ef4444', // red
  '#10b981', // emerald
  '#f59e0b', // amber
  '#8b5cf6', // violet
  '#ec4899', // pink
  '#06b6d4', // cyan
  '#f97316', // orange
  '#14b8a6', // teal
  '#6366f1', // indigo
  '#84cc16', // lime
  '#e11d48', // rose
  '#0ea5e9', // sky
  '#a855f7', // purple
  '#22c55e', // green
];

/**
 * Get a deterministic color for a process ID.
 * "Idle" always gets a gray color.
 */
export function getProcessColor(pid) {
  if (pid === 'Idle') return '#94a3b8';
  // Extract the number from the PID (e.g., "P1" → 1)
  const num = parseInt(pid.replace(/\D/g, ''), 10) || 0;
  return PROCESS_COLORS[num % PROCESS_COLORS.length];
}

/**
 * Generate random processes for quick testing.
 * @param {number} count - Number of processes
 * @returns {Array<Object>}
 */
export function generateRandomProcesses(count = 5) {
  const processes = [];
  for (let i = 1; i <= count; i++) {
    processes.push({
      pid: `P${i}`,
      arrival_time: Math.floor(Math.random() * 10),
      burst_time: Math.floor(Math.random() * 10) + 1, // 1-10
      priority: Math.floor(Math.random() * 10),
    });
  }
  return processes;
}

/**
 * Download a Blob as a file.
 */
export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

/**
 * Algorithm display names.
 */
export const ALGORITHM_LABELS = {
  fcfs: 'FCFS',
  sjf: 'SJF (Non-Preemptive)',
  srtf: 'SRTF (Preemptive SJF)',
  priority_np: 'Priority (Non-Preemptive)',
  priority_p: 'Priority (Preemptive)',
  round_robin: 'Round Robin',
  multilevel_queue: 'Multilevel Queue',
  mlfq: 'Multilevel Feedback Queue',
};

/**
 * Speed presets in milliseconds per time unit.
 */
export const SPEED_PRESETS = {
  Slow: 1000,
  Medium: 500,
  Fast: 150,
};

/**
 * Return a user-friendly error message from an Axios error.
 * Detects common issues like the backend not running.
 */
export function friendlyError(err) {
  if (err.code === 'ERR_NETWORK' || err.message === 'Network Error') {
    return 'Cannot reach the backend server. Make sure it is running (uvicorn app.main:app --reload --port 8000) and try again.';
  }
  return err.response?.data?.detail || err.message || 'Something went wrong';
}
