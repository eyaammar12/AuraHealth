import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, FlaskConical } from 'lucide-react';

export function ModeToggle({ mode, setMode }) {
  const isGemini = mode === 'gemini';

  return (
    <div className="flex items-center gap-3">
      <span className={`text-xs font-semibold uppercase tracking-wider transition-colors ${!isGemini ? 'text-blue-600' : 'text-slate-400'}`}>
        Mock
      </span>
      
      <button
        onClick={() => setMode(isGemini ? 'mock' : 'gemini')}
        className={`relative w-14 h-7 rounded-full transition-colors duration-300 focus:outline-none ${
          isGemini ? 'bg-blue-600' : 'bg-slate-200'
        }`}
      >
        <motion.div
          animate={{ x: isGemini ? 28 : 4 }}
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
          className="absolute top-1 w-5 h-5 bg-white rounded-full shadow-md flex items-center justify-center"
        >
          {isGemini ? (
            <Cpu size={12} className="text-blue-600" />
          ) : (
            <FlaskConical size={12} className="text-slate-400" />
          )}
        </motion.div>
      </button>

      <span className={`text-xs font-semibold uppercase tracking-wider transition-colors ${isGemini ? 'text-blue-600' : 'text-slate-400'}`}>
        Gemini
      </span>
    </div>
  );
}
