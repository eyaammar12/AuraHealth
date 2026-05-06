import { motion } from "framer-motion";
import { useNavigate, useLocation } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { AlertCircle, ArrowLeft, CheckCircle2, Clock, Activity, ShieldAlert } from "lucide-react";

export default function Results() {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Get data from navigation state
  const { result, inputData } = location.state || {};

  // Fallback if no data is present
  if (!result) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6 text-center">
        <Activity size={48} className="text-blue-500 mb-4 opacity-20" />
        <h1 className="text-2xl font-bold text-slate-900 mb-2">No Analysis Found</h1>
        <p className="text-slate-600 mb-8">Please complete the symptom assessment first.</p>
        <Button onClick={() => navigate("/symptoms")}>Start Assessment</Button>
      </div>
    );
  }

  const { possible_conditions, risk_level, advice, doctor_recommendation, disclaimer } = result;

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12">
      <div className="max-w-3xl mx-auto">
        <header className="flex items-center justify-between mb-8">
          <button 
            onClick={() => navigate("/symptoms")}
            className="flex items-center text-slate-500 hover:text-slate-900 transition-colors"
          >
            <ArrowLeft size={20} className="mr-1" />
            Edit Symptoms
          </button>
          
          <div className="flex items-center gap-2 opacity-60">
            <Activity size={18} />
            <span className="text-sm font-semibold tracking-tight">AuraHealth</span>
          </div>
        </header>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex items-center gap-3 mb-6">
            <h1 className="text-3xl font-bold text-slate-900">Analysis Complete</h1>
            <Badge variant={risk_level} className="px-3 py-1 text-sm capitalize">
              {risk_level} Risk
            </Badge>
          </div>
          
          <p className="text-slate-600 mb-8 leading-relaxed">
            Based on your reported symptoms ({inputData?.selectedSymptoms.join(", ")}) 
            with an intensity of {inputData?.intensity}/10, here are the most likely possibilities.
          </p>

          <div className="space-y-4 mb-8">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-2">Possible Conditions</h2>
            {possible_conditions.map((condition, index) => (
              <Card key={index} hover className="p-5 border-l-4 border-l-blue-500">
                <div className="flex justify-between items-start">
                  <h3 className="text-xl font-bold text-slate-900">{condition}</h3>
                  <Badge variant="neutral">AI Estimate</Badge>
                </div>
              </Card>
            ))}
          </div>

          <h2 className="text-xl font-bold text-slate-900 mb-4">Recommended Actions</h2>
          <Card className="p-0 mb-8 bg-white overflow-hidden">
            <ul className="divide-y divide-slate-100">
              {advice.map((item, index) => (
                <li key={index} className="p-4 flex items-start gap-3">
                  <CheckCircle2 className="text-blue-500 shrink-0 mt-0.5" size={20} />
                  <p className="text-slate-700">{item}</p>
                </li>
              ))}
            </ul>
          </Card>

          {doctor_recommendation && (
            <Card className="p-6 bg-gradient-to-br from-indigo-900 to-slate-900 text-white border-0 shadow-xl shadow-indigo-900/20 mb-8">
              <div className="flex items-start gap-4">
                <div className="bg-white/10 p-3 rounded-xl shrink-0">
                  <AlertCircle className="text-indigo-200" size={24} />
                </div>
                <div>
                  <h3 className="font-semibold text-lg mb-1">Doctor Recommendation</h3>
                  <p className="text-indigo-100 text-sm mb-4 leading-relaxed">
                    Given the severity of your symptoms, we strongly recommend consulting a healthcare provider for a professional evaluation.
                  </p>
                  <Button variant="secondary" className="bg-white text-indigo-900 hover:bg-slate-50 border-0">
                    Find a Doctor Nearby
                  </Button>
                </div>
              </div>
            </Card>
          )}

          <div className="flex items-center gap-3 p-4 bg-slate-100 rounded-xl text-slate-500 text-xs italic">
            <ShieldAlert size={16} />
            <p>{disclaimer}</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
