/**
 * Axios API client for the CPU Scheduling backend.
 * Base URL points to the FastAPI server.
 */

import axios from 'axios';

// In production (Vercel), API is on the same origin under /api.
// In development, Vite proxies /api to localhost:8000.
const API_BASE = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

/**
 * Schedule processes using a single algorithm.
 * @param {Object} payload - { processes, algorithm, time_quantum }
 * @returns {Promise<Object>} ScheduleResponse
 */
export const scheduleProcesses = (payload) =>
  api.post('/api/schedule', payload).then((res) => res.data);

/**
 * Compare multiple algorithms on the same input.
 * @param {Object} payload - { processes, time_quantum, algorithms? }
 * @returns {Promise<Object>} CompareResponse
 */
export const compareAlgorithms = (payload) =>
  api.post('/api/compare', payload).then((res) => res.data);

/**
 * Fetch algorithm metadata.
 * @returns {Promise<Array>} AlgorithmInfo[]
 */
export const getAlgorithms = () =>
  api.get('/api/algorithms').then((res) => res.data);

/**
 * Export single schedule result as CSV.
 * @param {Object} payload
 * @returns {Promise<Blob>}
 */
export const exportCSV = (payload) =>
  api.post('/api/export/csv', payload, { responseType: 'blob' }).then((res) => res.data);

/**
 * Export comparison results as CSV.
 * @param {Object} payload
 * @returns {Promise<Blob>}
 */
export const exportCompareCSV = (payload) =>
  api.post('/api/export/compare', payload, { responseType: 'blob' }).then((res) => res.data);

export default api;
