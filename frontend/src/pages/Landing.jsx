import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Activity } from "lucide-react";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50/50 to-white flex flex-col relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-400/10 blur-[100px]" />
      <div className="absolute top-[20%] right-[-10%] w-[30%] h-[30%] rounded-full bg-indigo-400/10 blur-[100px]" />

      <header className="px-6 py-6 flex items-center justify-between z-10">
        <div className="flex items-center gap-2">
          <div className="bg-blue-600 p-2 rounded-xl text-white">
            <Activity size={24} />
          </div>
          <span className="font-bold text-xl tracking-tight text-slate-900">AuraHealth</span>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-6 text-center z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: "easeOut" }}
          className="max-w-3xl"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-100/50 border border-blue-200 text-blue-700 text-sm font-medium mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
            AI-Powered Intelligence
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 tracking-tight leading-[1.1] mb-6">
            Understand your health with <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">clarity.</span>
          </h1>
          
          <p className="text-lg md:text-xl text-slate-600 mb-10 max-w-2xl mx-auto leading-relaxed">
            Get an instant, AI-driven pre-diagnosis by simply describing how you feel. Secure, fast, and remarkably accurate.
          </p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2, ease: "easeOut" }}
          >
            <Button 
              onClick={() => navigate("/symptoms")} 
              className="text-lg px-8 py-4 rounded-2xl shadow-xl shadow-blue-500/25 group"
            >
              Start Assessment
              <motion.span 
                className="ml-2 inline-block"
                initial={{ x: 0 }}
                whileHover={{ x: 4 }}
              >
                →
              </motion.span>
            </Button>
            <p className="mt-4 text-sm text-slate-500">Takes only 2 minutes. No sign up required.</p>
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
}
