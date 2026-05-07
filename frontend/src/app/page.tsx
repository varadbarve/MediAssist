"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Upload, 
  FileText, 
  Activity, 
  Phone, 
  CheckCircle2, 
  AlertCircle, 
  ChevronRight,
  Mic2,
  Stethoscope
} from "lucide-react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const API_URL = "https://mediassist-backend-1bom.onrender.com";

  const handleUpload = async () => {
    if (!file) return;
    setIsProcessing(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("patient_id", "PAT-12345");
    formData.append("patient_phone_number", "+919876543210");

    try {
      const response = await fetch(`${API_URL}/api/v1/reports/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Server error occurred");
      }

      const data = await response.json();
      setResult(data);
    } catch (error: any) {
      console.error("Upload failed", error);
      alert("⚠️ Analysis Failed: " + error.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.6, staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { opacity: 1, scale: 1 }
  };

  return (
    <main className="min-h-screen bg-[#09090b] text-zinc-100 selection:bg-blue-500/30 overflow-x-hidden">
      {/* Background Glow */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full" />
        <div className="absolute top-[20%] -right-[10%] w-[30%] h-[30%] bg-emerald-600/10 blur-[120px] rounded-full" />
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12 relative z-10">
        {/* Header */}
        <header className="mb-16 text-center">
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold uppercase tracking-wider mb-4"
          >
            <Activity className="w-3 h-3" />
            AI-Powered Healthcare
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-5xl md:text-7xl font-bold tracking-tighter bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent mb-4"
          >
            MediAssist AI
          </motion.h1>
          <p className="text-zinc-500 text-lg max-w-2xl mx-auto leading-relaxed">
            Revolutionizing patient follow-ups with automated medical report analysis and intelligent voice simulations.
          </p>
        </header>

        <div className="grid lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Upload */}
          <div className="lg:col-span-5 space-y-6 relative">
            <div className="group relative p-8 rounded-3xl bg-zinc-900/50 border border-zinc-800 hover:border-zinc-700 transition-all duration-500 backdrop-blur-xl">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-3xl pointer-events-none" />
              
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                <FileText className="w-5 h-5 text-blue-400" />
                Upload Lab Report
              </h2>

              <div 
                className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ${
                  file ? 'border-emerald-500/50 bg-emerald-500/5' : 'border-zinc-800 hover:border-blue-500/50 bg-zinc-950/50'
                }`}
              >
                <input 
                  type="file" 
                  id="file-upload"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-20" 
                  onChange={(e) => {
                    const selectedFile = e.target.files?.[0] || null;
                    console.log("File selected:", selectedFile);
                    setFile(selectedFile);
                  }}
                  accept=".pdf"
                />
                
                <div className="space-y-4 relative z-10">
                  <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mx-auto border transition-all duration-500 ${
                    file ? 'bg-emerald-500/20 border-emerald-500/50 scale-110' : 'bg-zinc-900 border-zinc-800'
                  }`}>
                    {file ? <CheckCircle2 className="w-8 h-8 text-emerald-400" /> : <Upload className="w-8 h-8 text-blue-400" />}
                  </div>
                  <div>
                    <p className={`font-bold transition-colors ${file ? 'text-emerald-400' : 'text-zinc-200'}`}>
                      {file ? file.name : "Select your PDF report"}
                    </p>
                    <p className="text-sm text-zinc-500 mt-1">
                      {file ? "File ready for analysis" : "Drag and drop or click to browse"}
                    </p>
                  </div>
                </div>
              </div>

              <button 
                type="button"
                id="analyze-button"
                onClick={() => {
                  console.log("Analyze button clicked!");
                  handleUpload();
                }}
                disabled={!file || isProcessing}
                className="w-full mt-8 py-4 px-6 rounded-2xl bg-white text-black font-bold flex items-center justify-center gap-2 hover:bg-zinc-200 disabled:bg-zinc-800 disabled:text-zinc-500 disabled:cursor-not-allowed transition-all active:scale-[0.98] cursor-pointer relative z-50"
              >
                {isProcessing ? (
                  <div className="w-5 h-5 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                ) : (
                  <>
                    Analyze Report & Start Call
                    <ChevronRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>

            {/* Quick Stats/Info */}
            <div className="grid grid-cols-2 gap-4">
              <div className="p-6 rounded-3xl bg-zinc-900/30 border border-zinc-800/50">
                <Mic2 className="w-5 h-5 text-purple-400 mb-3" />
                <p className="text-xs text-zinc-500 font-bold uppercase mb-1">AI Voice</p>
                <p className="text-sm text-zinc-300">Neural Engine v2.0</p>
              </div>
              <div className="p-6 rounded-3xl bg-zinc-900/30 border border-zinc-800/50">
                <Stethoscope className="w-5 h-5 text-emerald-400 mb-3" />
                <p className="text-xs text-zinc-500 font-bold uppercase mb-1">Privacy</p>
                <p className="text-sm text-zinc-300">HIPAA Compliant</p>
              </div>
            </div>
          </div>

          {/* Right Column: Results */}
          <div className="lg:col-span-7">
            <AnimatePresence mode="wait">
              {result ? (
                <motion.div 
                  key="results"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-6"
                >
                  <div className="p-5 sm:p-8 rounded-3xl bg-zinc-900/50 border border-zinc-800 backdrop-blur-xl">
                    <div className="flex items-center justify-between mb-8">
                      <h2 className="text-xl sm:text-2xl font-bold tracking-tight">Analysis Results</h2>
                      <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] font-bold uppercase tracking-widest border border-emerald-500/20">
                        Completed
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
                      {Object.entries(result.extracted_data || {}).map(([key, val]: any) => {
                        const num = parseFloat(val);
                        let colorClass = "text-emerald-400";
                        if (key === "Hemoglobin") {
                          if (num < 10) colorClass = "text-red-400";
                          else if (num < 12) colorClass = "text-yellow-400";
                        } else if (key === "Vitamin_B12") {
                          if (num < 100) colorClass = "text-red-400";
                          else if (num < 200) colorClass = "text-yellow-400";
                        }
                        // ... add other ranges as needed

                        return (
                          <motion.div 
                            key={key}
                            variants={itemVariants}
                            className="p-4 sm:p-5 rounded-2xl bg-zinc-950/50 border border-zinc-800/50 group hover:border-blue-500/30 transition-all duration-300"
                          >
                            <p className="text-[10px] text-zinc-500 uppercase font-black tracking-widest mb-1">
                              {key.replace('_', ' ')}
                            </p>
                            <p className={`text-2xl sm:text-3xl font-mono font-bold ${colorClass}`}>
                              {val}
                            </p>
                          </motion.div>
                        );
                      })}
                    </div>

                    <div className="space-y-6">
                      <div className="space-y-3">
                        <h3 className="text-xs font-black text-zinc-500 uppercase tracking-[0.2em]">Patient Summary</h3>
                        <div className="p-4 sm:p-6 rounded-2xl bg-blue-500/5 border border-blue-500/10 text-zinc-300 leading-relaxed text-base sm:text-lg whitespace-pre-line break-words">
                          {result.ai_summary}
                        </div>
                      </div>

                      {result.full_script && (
                        <div className="space-y-3">
                          <h3 className="text-xs font-black text-zinc-500 uppercase tracking-[0.2em]">Automated Call Transcript</h3>
                          <div className="p-4 sm:p-6 rounded-2xl bg-zinc-950/50 border border-zinc-800/50 text-zinc-400 text-xs sm:text-sm leading-relaxed font-mono whitespace-pre-line break-words">
                            {result.full_script}
                          </div>
                        </div>
                      )}

                      <div className="pt-6 border-t border-zinc-800 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full bg-blue-500/10 flex items-center justify-center">
                            <Phone className="w-5 h-5 text-blue-400" />
                          </div>
                          <div>
                            <p className="text-xs font-bold text-zinc-200">Call Simulation</p>
                            <p className="text-[10px] text-zinc-500 uppercase">Live Playback</p>
                          </div>
                        </div>
                        
                        {result.call_status.audio_base64 && (
                          <audio 
                            controls 
                            className="h-10 rounded-full invert hue-rotate-180 brightness-150 opacity-80 hover:opacity-100 transition-opacity"
                            src={`data:audio/mp3;base64,${result.call_status.audio_base64}`}
                          />
                        )}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ) : (
                <motion.div 
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="h-full flex flex-col items-center justify-center p-12 text-center rounded-3xl border-2 border-dashed border-zinc-800 bg-zinc-900/10"
                >
                  <div className="w-20 h-20 bg-zinc-900 rounded-full flex items-center justify-center mb-6 border border-zinc-800">
                    <Activity className="w-10 h-10 text-zinc-700" />
                  </div>
                  <h3 className="text-xl font-bold text-zinc-400 mb-2">Ready for Analysis</h3>
                  <p className="text-zinc-500 max-w-xs">
                    Upload a medical report to see AI insights and hear the automated patient call.
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-20 pt-8 border-t border-zinc-900 text-center">
          <p className="text-zinc-600 text-xs uppercase tracking-widest font-bold">
            MediAssist AI &bull; Smart Healthcare Systems &bull; 2026
          </p>
        </footer>
      </div>
    </main>
  );
}
