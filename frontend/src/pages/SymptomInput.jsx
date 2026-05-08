import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { ChevronLeft, Info, Loader2 } from "lucide-react";
import { analyzeSymptoms } from "../services/api";

const commonSymptoms = [
  "Headache", "Fever", "Cough", "Fatigue", "Nausea", 
  "Dizziness", "Shortness of breath", "Muscle ache", "Sore throat", "Chest pain"
];

export default function SymptomInput() {
  const navigate = useNavigate();
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [intensity, setIntensity] = useState(5);
  const [duration, setDuration] = useState(1);
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const toggleSymptom = (symptom) => {
    if (selectedSymptoms.includes(symptom)) {
      setSelectedSymptoms(selectedSymptoms.filter(s => s !== symptom));
    } else {
      setSelectedSymptoms([...selectedSymptoms, symptom]);
    }
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeSymptoms({
        symptoms: selectedSymptoms,
        severity: intensity,
        duration: duration,
        notes: notes
      });
      
      // Navigate to results page and pass the data via state
      navigate("/results", { state: { result, inputData: { selectedSymptoms, intensity, duration } } });
    } catch (err) {
      setError("Failed to analyze symptoms. Please make sure the backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12">
      <div className="max-w-2xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <button 
            onClick={() => navigate("/")}
            className="flex items-center text-slate-500 hover:text-slate-900 transition-colors"
            disabled={loading}
          >
            <ChevronLeft size={20} className="mr-1" />
            Back
          </button>
        </div>

        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">How are you feeling?</h1>
          <p className="text-slate-600">Select your symptoms so we can assess your condition.</p>
        </div>

        <Card className="p-6 md:p-8 mb-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">1. What are your symptoms?</h2>
          <div className="flex flex-wrap gap-2 mb-6">
            {commonSymptoms.map(symptom => {
              const isSelected = selectedSymptoms.includes(symptom);
              return (
                <motion.button
                  key={symptom}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => toggleSymptom(symptom)}
                  className={`px-4 py-2 rounded-full text-sm font-medium border transition-colors ${
                    isSelected 
                      ? "bg-blue-600 text-white border-blue-600 shadow-sm" 
                      : "bg-white text-slate-700 border-slate-200 hover:border-blue-300"
                  }`}
                  disabled={loading}
                >
                  {symptom}
                </motion.button>
              );
            })}
          </div>

          <div className="h-px bg-slate-100 my-8" />

          <h2 className="text-lg font-semibold text-slate-900 mb-4">2. Intensity level</h2>
          <div className="mb-8">
            <div className="flex justify-between text-sm text-slate-500 mb-2">
              <span>Mild</span>
              <span className="font-medium text-slate-900">{intensity} / 10</span>
              <span>Severe</span>
            </div>
            <input 
              type="range" 
              min="1" max="10" 
              value={intensity}
              onChange={(e) => setIntensity(parseInt(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              disabled={loading}
            />
          </div>

          <div className="h-px bg-slate-100 my-8" />

          <h2 className="text-lg font-semibold text-slate-900 mb-4">3. Details</h2>
          
          <div className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Duration (days)</label>
              <input 
                type="number"
                min="1"
                value={duration}
                onChange={(e) => setDuration(parseInt(e.target.value) || 1)}
                className="w-full border-slate-200 rounded-xl shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white px-4 py-2.5 text-sm outline-none border"
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Additional context (optional)</label>
              <textarea 
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Any other details you want to share..."
                rows={3}
                className="w-full border-slate-200 rounded-xl shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-white px-4 py-3 text-sm outline-none border resize-none"
                disabled={loading}
              />
            </div>
          </div>
        </Card>

        {error && (
          <div className="bg-rose-50 text-rose-700 p-4 rounded-xl mb-6 border border-rose-100 text-sm">
            {error}
          </div>
        )}

        <div className="flex items-center bg-blue-50 text-blue-800 p-4 rounded-xl mb-8 border border-blue-100">
          <Info size={20} className="mr-3 shrink-0 text-blue-500" />
          <p className="text-sm">This is an AI pre-diagnosis tool and does not replace professional medical advice.</p>
        </div>

        <Button 
          fullWidth 
          onClick={handleAnalyze}
          disabled={selectedSymptoms.length === 0 || loading}
          className="py-4 text-base rounded-2xl shadow-lg shadow-blue-500/20 flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              Analyzing with AI...
            </>
          ) : (
            "Analyze Symptoms"
          )}
        </Button>
      </div>
    </div>
  );
}
