import { motion } from "framer-motion";

export function Card({ children, className = "", hover = false, ...props }) {
  const hoverProps = hover ? {
    whileHover: { y: -4, boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)" },
    transition: { type: "spring", stiffness: 300, damping: 20 }
  } : {};

  return (
    <motion.div 
      className={`bg-white rounded-2xl shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-slate-100 overflow-hidden ${className}`}
      {...hoverProps}
      {...props}
    >
      {children}
    </motion.div>
  );
}
