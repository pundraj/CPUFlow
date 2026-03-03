/**
 * AlgorithmInfo – displays a brief description and time complexity
 * of the currently selected algorithm.
 */

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const INFO = {
  fcfs: {
    name: 'First Come First Serve (FCFS)',
    desc: 'Processes are executed in the order they arrive. Simple but can cause the "convoy effect" where short processes wait behind long ones.',
    complexity: 'O(n log n)',
    preemptive: false,
    pros: ['Simple to implement', 'No starvation'],
    cons: ['High average waiting time', 'Convoy effect'],
  },
  sjf: {
    name: 'Shortest Job First (SJF)',
    desc: 'Selects the process with the shortest burst time among those that have arrived. Optimal for minimizing average waiting time (non-preemptive).',
    complexity: 'O(n²)',
    preemptive: false,
    pros: ['Minimum average waiting time', 'Optimal for batch systems'],
    cons: ['Starvation of long processes', 'Requires burst time prediction'],
  },
  srtf: {
    name: 'Shortest Remaining Time First (SRTF)',
    desc: 'Preemptive version of SJF. At every time unit, the process with the smallest remaining burst time gets the CPU.',
    complexity: 'O(n × T)',
    preemptive: true,
    pros: ['Better avg. waiting time than SJF', 'Responsive to short jobs'],
    cons: ['High overhead from frequent switching', 'Starvation possible'],
  },
  priority_np: {
    name: 'Priority Scheduling (Non-Preemptive)',
    desc: 'Each process has a priority. The highest-priority (lowest number) ready process runs next and finishes before another is selected.',
    complexity: 'O(n²)',
    preemptive: false,
    pros: ['Supports process importance', 'Straightforward'],
    cons: ['Starvation of low-priority processes', 'Priority inversion'],
  },
  priority_p: {
    name: 'Priority Scheduling (Preemptive)',
    desc: 'Like non-preemptive priority, but a newly arrived higher-priority process can preempt the currently running one.',
    complexity: 'O(n × T)',
    preemptive: true,
    pros: ['Responsive to high-priority tasks', 'Better for real-time systems'],
    cons: ['Starvation', 'Context switching overhead'],
  },
  round_robin: {
    name: 'Round Robin (RR)',
    desc: 'Each process gets a fixed time quantum in cyclic order. If it doesn\'t finish, it goes to the back of the queue. Fair and widely used in time-sharing systems.',
    complexity: 'O(n × T/Q)',
    preemptive: true,
    pros: ['Fair – no starvation', 'Good response time', 'Simple'],
    cons: ['Performance depends on quantum choice', 'Higher overhead'],
  },
  multilevel_queue: {
    name: 'Multilevel Queue Scheduling',
    desc: 'Processes are permanently assigned to one of several queues based on priority. Each queue has its own scheduling algorithm. Higher queues preempt lower ones.',
    complexity: 'O(n × T)',
    preemptive: true,
    pros: ['Separates process types', 'Efficient for known workloads'],
    cons: ['Inflexible – no queue migration', 'Starvation of lower queues'],
  },
  mlfq: {
    name: 'Multilevel Feedback Queue (MLFQ)',
    desc: 'Like multilevel queue, but processes can move between queues. A process using too much CPU is demoted; I/O-bound processes stay in high-priority queues.',
    complexity: 'O(n × T)',
    preemptive: true,
    pros: ['Adaptive to process behavior', 'Balances responsiveness & throughput'],
    cons: ['Complex to tune', 'Potential gaming of the system'],
  },
};

export default function AlgorithmInfoPanel({ algorithm }) {
  const info = INFO[algorithm];
  if (!info) return null;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={algorithm}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.2 }}
        className="card p-4"
      >
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-semibold">{info.name}</h3>
          <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
            info.preemptive
              ? 'bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-300'
              : 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
          }`}>
            {info.preemptive ? 'Preemptive' : 'Non-Preemptive'}
          </span>
        </div>
        <p className="text-xs mb-3" style={{ color: 'var(--text-secondary)' }}>{info.desc}</p>
        <div className="text-[11px] font-mono mb-3 px-2 py-1 rounded inline-block"
          style={{ backgroundColor: 'var(--bg-primary)' }}>
          Time Complexity: {info.complexity}
        </div>
        <div className="grid grid-cols-2 gap-3 text-[11px]">
          <div>
            <div className="font-semibold text-green-500 mb-1">✓ Pros</div>
            <ul className="space-y-0.5" style={{ color: 'var(--text-secondary)' }}>
              {info.pros.map((p) => <li key={p}>• {p}</li>)}
            </ul>
          </div>
          <div>
            <div className="font-semibold text-red-500 mb-1">✗ Cons</div>
            <ul className="space-y-0.5" style={{ color: 'var(--text-secondary)' }}>
              {info.cons.map((c) => <li key={c}>• {c}</li>)}
            </ul>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
