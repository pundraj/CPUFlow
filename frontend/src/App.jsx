/**
 * App – root component.
 * Wraps everything with dark mode context and the main layout.
 */

import React from 'react';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import useDarkMode from './hooks/useDarkMode';

export default function App() {
  const { dark, toggle } = useDarkMode();

  return (
    <div className="min-h-screen flex flex-col transition-colors duration-300"
      style={{ backgroundColor: 'var(--bg-primary)', color: 'var(--text-primary)' }}>
      <Header dark={dark} toggleDark={toggle} />
      <main className="flex-1">
        <Dashboard />
      </main>

      {/* Footer */}
      <footer className="text-center py-4 text-[11px] border-t"
        style={{ borderColor: 'var(--border-color)', color: 'var(--text-secondary)' }}>
        CPU Scheduling Algorithm Visualizer · Built with React, Tailwind CSS, FastAPI
      </footer>
    </div>
  );
}
