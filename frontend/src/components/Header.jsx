/**
 * Header component with app title and dark/light mode toggle.
 */

import React from 'react';
import { motion } from 'framer-motion';

export default function Header({ dark, toggleDark }) {
  return (
    <header className="sticky top-0 z-50 backdrop-blur-md border-b"
      style={{ borderColor: 'var(--border-color)', backgroundColor: dark ? 'rgba(15,23,42,0.85)' : 'rgba(248,250,252,0.85)' }}>
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
        {/* Logo & title */}
        <div className="flex items-center gap-3">
          <motion.div
            className="w-9 h-9 rounded-lg bg-primary-600 flex items-center justify-center text-white font-bold text-lg"
            whileHover={{ rotate: 10, scale: 1.05 }}
          >
            S
          </motion.div>
          <div>
            <h1 className="text-lg font-bold leading-tight">CPU Scheduler</h1>
            <p className="text-[11px] hidden sm:block" style={{ color: 'var(--text-secondary)' }}>
              Interactive OS Scheduling Visualizer
            </p>
          </div>
        </div>

        {/* Dark mode toggle */}
        <button
          onClick={toggleDark}
          className="p-2 rounded-lg transition-colors hover:bg-gray-200 dark:hover:bg-gray-700"
          aria-label="Toggle dark mode"
        >
          {dark ? (
            <svg className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd"
                d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                clipRule="evenodd" />
            </svg>
          ) : (
            <svg className="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
            </svg>
          )}
        </button>
      </div>
    </header>
  );
}
