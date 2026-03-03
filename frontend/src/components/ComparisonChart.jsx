/**
 * ComparisonChart – bar chart comparing average metrics across algorithms.
 *
 * Uses Recharts to render grouped bar charts for:
 *  - Average Waiting Time
 *  - Average Turnaround Time
 *  - CPU Utilization
 *  - Throughput
 */

import React, { useMemo } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const CHART_COLORS = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b'];

export default function ComparisonChart({ comparisonResults }) {
  const data = useMemo(() => {
    if (!comparisonResults) return [];
    return Object.entries(comparisonResults).map(([key, result]) => ({
      algorithm: result.algorithm.length > 20
        ? result.algorithm.replace(/\(.*?\)/g, '').trim()
        : result.algorithm,
      'Avg Wait': result.metrics.average_waiting_time,
      'Avg TAT': result.metrics.average_turnaround_time,
      'CPU Util %': result.metrics.cpu_utilization,
      Throughput: result.metrics.throughput,
    }));
  }, [comparisonResults]);

  if (!comparisonResults || data.length === 0) {
    return (
      <div className="card p-6 flex items-center justify-center h-40">
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Use "Compare All Algorithms" to see charts
        </p>
      </div>
    );
  }

  const metrics = ['Avg Wait', 'Avg TAT', 'CPU Util %', 'Throughput'];

  return (
    <div className="card p-4">
      <h3 className="text-sm font-semibold mb-4">Algorithm Comparison</h3>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {metrics.map((metric, i) => (
          <div key={metric}>
            <h4 className="text-xs font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
              {metric}
            </h4>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis
                  dataKey="algorithm"
                  tick={{ fontSize: 9, fill: 'var(--text-secondary)' }}
                  interval={0}
                  angle={-20}
                  textAnchor="end"
                  height={60}
                />
                <YAxis tick={{ fontSize: 10, fill: 'var(--text-secondary)' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--bg-secondary)',
                    border: '1px solid var(--border-color)',
                    borderRadius: 8,
                    fontSize: 11,
                  }}
                />
                <Bar dataKey={metric} fill={CHART_COLORS[i]} radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ))}
      </div>

      {/* Fairness analysis */}
      <FairnessAnalysis data={data} />
    </div>
  );
}


/**
 * FairnessAnalysis – simple variance-based fairness indicator.
 */
function FairnessAnalysis({ data }) {
  if (data.length === 0) return null;

  // Calculate coefficient of variation for waiting times per algorithm
  const waitValues = data.map((d) => d['Avg Wait']);
  const mean = waitValues.reduce((a, b) => a + b, 0) / waitValues.length;
  const variance = waitValues.reduce((sum, v) => sum + (v - mean) ** 2, 0) / waitValues.length;
  const stdDev = Math.sqrt(variance);
  const cv = mean > 0 ? ((stdDev / mean) * 100).toFixed(1) : 0;

  // Find best & worst
  const best = data.reduce((min, d) => (d['Avg Wait'] < min['Avg Wait'] ? d : min), data[0]);
  const worst = data.reduce((max, d) => (d['Avg Wait'] > max['Avg Wait'] ? d : max), data[0]);

  return (
    <div className="mt-4 pt-4 border-t" style={{ borderColor: 'var(--border-color)' }}>
      <h4 className="text-xs font-semibold mb-2">Fairness & Analysis</h4>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div className="p-2 rounded-lg" style={{ backgroundColor: 'var(--bg-primary)' }}>
          <div className="text-[10px] uppercase mb-1" style={{ color: 'var(--text-secondary)' }}>Best Avg Wait</div>
          <div className="font-bold text-green-500">{best.algorithm}: {best['Avg Wait']}</div>
        </div>
        <div className="p-2 rounded-lg" style={{ backgroundColor: 'var(--bg-primary)' }}>
          <div className="text-[10px] uppercase mb-1" style={{ color: 'var(--text-secondary)' }}>Worst Avg Wait</div>
          <div className="font-bold text-red-500">{worst.algorithm}: {worst['Avg Wait']}</div>
        </div>
        <div className="p-2 rounded-lg" style={{ backgroundColor: 'var(--bg-primary)' }}>
          <div className="text-[10px] uppercase mb-1" style={{ color: 'var(--text-secondary)' }}>Variance (CV)</div>
          <div className="font-bold">{cv}%</div>
        </div>
      </div>
    </div>
  );
}
