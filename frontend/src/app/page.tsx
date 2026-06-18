"use client";

import { useState, useEffect } from "react";
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
  Stethoscope,
  LogOut,
  Shield
} from "lucide-react";
import { isAuthenticated, getAuthHeaders, getUser, logout } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [patientId, setPatientId] = useState("");
  const [patientPhone, setPatientPhone] = useState("");
  const [prescriptionNotes, setPrescriptionNotes] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [authChecked, setAuthChecked] = useState(false);
  const router = useRouter();
  const user = getUser();

  const [pendingReports, setPendingReports] = useState<any[]>([]);
  const [selectedReportIds, setSelectedReportIds] = useState<string[]>([]);
  const [isCosigning, setIsCosigning] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://mediassist-backend-1bom.onrender.com";

  const fetchPendingReports = async () => {
    try {
      const response = await fetch(`${API_URL}/api/v1/reports/pending-cosignature`, {
        headers: getAuthHeaders(),
      });
      if (response.ok) {
        const data = await response.json();
        setPendingReports(data);
      }
    } catch (err) {
      console.error("Failed to fetch pending reports", err);
    }
  };

  useEffect(() => {
    if (authChecked && user?.role === "doctor") {
      fetchPendingReports();
      // Poll every 10 seconds for new submissions from interns
      const interval = setInterval(fetchPendingReports, 10000);
      return () => clearInterval(interval);
    }
  }, [authChecked]);

  const handleCosignSelected = async (ids?: string[]) => {
    const targetIds = ids || selectedReportIds;
    if (targetIds.length === 0) return;
    setIsCosigning(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/reports/cosign`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...getAuthHeaders(),
        },
        body: JSON.stringify({ report_ids: targetIds }),
      });
      if (response.ok) {
        alert("Selected reports co-signed successfully! Outbound calls initiated.");
        setSelectedReportIds([]);
        fetchPendingReports();
      } else {
        alert("Failed to co-sign reports.");
      }
    } catch (err) {
      console.error(err);
      alert("Error occurred during co-signing.");
    } finally {
      setIsCosigning(false);
    }
  };

  // --- Layer 9: Auth Protection ---
  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/login");
    } else {
      setAuthChecked(true);
    }
  }, [router]);

  const handleUpload = async () => {
    if (!file || !patientId || !patientPhone || !prescriptionNotes) return;
    setIsProcessing(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("patient_id", patientId);
    formData.append("patient_phone_number", patientPhone);
    formData.append("prescription_notes", prescriptionNotes);

    try {
      const response = await fetch(`${API_URL}/api/v1/reports/upload`, {
        method: "POST",
        headers: {
          // --- Layer 9: Send JWT token with every API request ---
          ...getAuthHeaders(),
        },
        body: formData,
      });

      if (response.status === 401) {
        // Token expired or invalid — redirect to login
        logout();
        return;
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Server error occurred");
      }

      const data = await response.json();
      setResult(data);
    } catch (error: any) {
      console.error("Upload failed", error);
      alert("Analysis Failed: " + error.message);
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

  // Don't render until auth check is complete
  if (!authChecked) {
    return (
      <main className="min-h-screen bg-[#09090b] flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-zinc-700 border-t-blue-400 rounded-full animate-spin" />
      </main>
    );
  }

  // --- Layer 9: Conditional Patient Portal View ---
  if (user?.role === "patient") {
    return (
      <main className="min-h-screen bg-[#09090b] text-zinc-100 relative overflow-hidden pb-12">
        {/* Background Glow */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-[20%] -right-[10%] w-[50%] h-[50%] bg-emerald-600/5 blur-[150px] rounded-full" />
          <div className="absolute bottom-[10%] -left-[10%] w-[40%] h-[40%] bg-blue-600/5 blur-[150px] rounded-full" />
        </div>

        <div className="max-w-6xl mx-auto px-6 py-12 relative z-10">
          {/* Header */}
          <header className="pb-8 mb-12 border-b border-zinc-900">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-blue-500/20 border border-emerald-500/30 flex items-center justify-center">
                  <Activity className="w-5 h-5 text-emerald-400" />
                </div>
                <div>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-widest font-black">Patient Portal</p>
                  <p className="text-sm font-bold text-zinc-300">{user?.full_name}</p>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold">
                  <Shield className="w-3 h-3" />
                  Secure Access
                </div>
                <button
                  onClick={logout}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-zinc-800 text-zinc-500 text-xs font-bold hover:bg-red-500/10 hover:border-red-500/20 hover:text-red-400 transition-all"
                >
                  <LogOut className="w-3 h-3" />
                  Logout
                </button>
              </div>
            </div>

            <div className="text-center mt-12">
              <h1 className="text-4xl md:text-6xl font-bold tracking-tight bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent mb-4">
                Welcome to MediAssist
              </h1>
              <p className="text-zinc-500 text-base max-w-xl mx-auto">
                Your personal health dashboard for reviewing report summaries, prescriptions, and outbound voice follow-ups.
              </p>
            </div>
          </header>

          {/* 2x2 Balanced Grid */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* Card 1: My Health Records */}
            <div className="p-8 rounded-3xl bg-zinc-900/40 border border-zinc-800 backdrop-blur-xl relative overflow-hidden group hover:border-emerald-500/30 transition-all duration-300">
              <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none">
                <FileText className="w-24 h-24 text-emerald-400" />
              </div>
              <h3 className="text-lg font-bold text-zinc-200 mb-6 flex items-center gap-2">
                <FileText className="w-5 h-5 text-emerald-400" />
                Latest Health Indicators
              </h3>
              
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/60">
                  <span className="text-sm text-zinc-400 font-medium">Hemoglobin</span>
                  <span className="text-lg font-mono font-bold text-emerald-400">13.5 g/dL</span>
                </div>
                <div className="flex justify-between items-center p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/60">
                  <span className="text-sm text-zinc-400 font-medium">Cholesterol</span>
                  <span className="text-lg font-mono font-bold text-emerald-400">180 mg/dL</span>
                </div>
                <div className="flex justify-between items-center p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/60">
                  <span className="text-sm text-zinc-400 font-medium">Vitamin D3</span>
                  <span className="text-lg font-mono font-bold text-emerald-400">32.0 ng/mL</span>
                </div>
              </div>
              <p className="text-[10px] text-zinc-500 uppercase tracking-wider font-bold mt-6 text-center">
                Last checked: Today &bull; Status: Healthy
              </p>
            </div>

            {/* Card 2: Active Prescriptions */}
            <div className="p-8 rounded-3xl bg-zinc-900/40 border border-zinc-800 backdrop-blur-xl relative overflow-hidden group hover:border-blue-500/30 transition-all duration-300">
              <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none">
                <Activity className="w-24 h-24 text-blue-400" />
              </div>
              <h3 className="text-lg font-bold text-zinc-200 mb-6 flex items-center gap-2">
                <Activity className="w-5 h-5 text-blue-400" />
                Active Prescriptions
              </h3>

              <div className="p-5 rounded-2xl bg-blue-500/5 border border-blue-500/10 text-zinc-300 text-sm leading-relaxed mb-6">
                Take 1 Vitamin D3 pill daily after breakfast. Ensure you drink plenty of water throughout the day.
              </div>

              <div className="space-y-2 text-xs text-zinc-500 font-medium">
                <div className="flex justify-between">
                  <span>Prescribing Clinician:</span>
                  <span className="text-zinc-300 font-bold">Dr. Jane Smith</span>
                </div>
                <div className="flex justify-between">
                  <span>Dosage Timing:</span>
                  <span className="text-zinc-300 font-bold">Daily (After Meals)</span>
                </div>
              </div>
              <p className="text-[10px] text-zinc-500 uppercase tracking-wider font-bold mt-6 text-center">
                Active Status: Verified
              </p>
            </div>

            {/* Card 3: Voice Call Follow-Up */}
            <div className="p-8 rounded-3xl bg-zinc-900/40 border border-zinc-800 backdrop-blur-xl relative overflow-hidden group hover:border-purple-500/30 transition-all duration-300">
              <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none">
                <Phone className="w-24 h-24 text-purple-400" />
              </div>
              <h3 className="text-lg font-bold text-zinc-200 mb-6 flex items-center gap-2">
                <Phone className="w-5 h-5 text-purple-400" />
                AI Voice Follow-Up
              </h3>

              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-xs text-zinc-500 font-bold uppercase">Simulation Status:</span>
                  <span className="px-2 py-0.5 rounded bg-purple-500/10 border border-purple-500/20 text-purple-400 text-[10px] font-bold uppercase">
                    Completed
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-zinc-500 font-bold uppercase">Call Timestamp:</span>
                  <span className="text-zinc-300 text-xs font-mono font-bold">Today, 7:56 PM</span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/60 text-xs text-zinc-400 leading-relaxed font-mono mb-4">
                "Hello, this is a message from your clinic regarding your recent report. Many of your levels look stable and healthy. Your doctor has prescribed..."
              </div>

              <p className="text-[10px] text-zinc-500 uppercase tracking-wider font-bold mt-2 text-center">
                Interactive voice support is fully operational
              </p>
            </div>

            {/* Card 4: Support & Escalation */}
            <div className="p-8 rounded-3xl bg-zinc-900/40 border border-zinc-800 backdrop-blur-xl relative overflow-hidden group hover:border-yellow-500/30 transition-all duration-300">
              <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none">
                <Stethoscope className="w-24 h-24 text-yellow-400" />
              </div>
              <h3 className="text-lg font-bold text-zinc-200 mb-6 flex items-center gap-2">
                <Stethoscope className="w-5 h-5 text-yellow-400" />
                Clinic Support
              </h3>

              <p className="text-zinc-400 text-sm leading-relaxed mb-6">
                Need to speak with a human clinician or change your prescription? Request a callback directly below.
              </p>

              <button 
                onClick={() => alert("Clinic notified! A staff member will call you shortly.")}
                className="w-full py-3 px-4 rounded-xl border border-yellow-500/30 bg-yellow-500/10 text-yellow-400 font-bold text-sm hover:bg-yellow-500/20 transition-all active:scale-[0.98]"
              >
                Request Doctor Callback
              </button>

              <p className="text-[10px] text-zinc-500 uppercase tracking-wider font-bold mt-6 text-center">
                Typical response time: &lt;15 mins
              </p>
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

  return (
    <main className="min-h-screen bg-[#09090b] text-zinc-100 selection:bg-blue-500/30 overflow-x-hidden">
      {/* Background Glow */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full" />
        <div className="absolute top-[20%] -right-[10%] w-[30%] h-[30%] bg-emerald-600/10 blur-[120px] rounded-full" />
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12 relative z-10">
        {/* Header */}
        <header className="mb-16">
          <div className="flex items-center justify-between mb-8">
            {/* User Info */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-3"
            >
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-emerald-500 flex items-center justify-center text-sm font-bold">
                {user?.full_name?.charAt(0)?.toUpperCase() || "U"}
              </div>
              <div>
                <p className="text-sm font-bold text-zinc-200">{user?.full_name || "User"}</p>
                <p className="text-xs text-zinc-500">{user?.role?.toUpperCase()} &bull; {user?.email}</p>
              </div>
            </motion.div>

            {/* Auth Badge + Logout */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-3"
            >
              <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold">
                <Shield className="w-3 h-3" />
                Authenticated
              </div>
              <button
                onClick={logout}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-zinc-800 text-zinc-500 text-xs font-bold hover:bg-red-500/10 hover:border-red-500/20 hover:text-red-400 transition-all"
              >
                <LogOut className="w-3 h-3" />
                Logout
              </button>
            </motion.div>
          </div>

          <div className="text-center">
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
          </div>
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

              {/* Dynamic Patient & Prescription Inputs */}
              <div className="mt-6 space-y-4 text-left">
                <div className="space-y-1">
                  <label className="text-[10px] font-black text-zinc-500 uppercase tracking-wider" htmlFor="patient-id">
                    Patient ID
                  </label>
                  <input
                    id="patient-id"
                    type="text"
                    value={patientId}
                    onChange={(e) => setPatientId(e.target.value)}
                    placeholder="e.g. PAT-12345"
                    className="w-full px-4 py-2.5 bg-zinc-950/50 border border-zinc-800 rounded-xl text-sm text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:border-blue-500/50 transition-all"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[10px] font-black text-zinc-500 uppercase tracking-wider" htmlFor="patient-phone">
                    Patient Phone Number
                  </label>
                  <input
                    id="patient-phone"
                    type="tel"
                    value={patientPhone}
                    onChange={(e) => setPatientPhone(e.target.value)}
                    placeholder="e.g. +919876543210"
                    className="w-full px-4 py-2.5 bg-zinc-950/50 border border-zinc-800 rounded-xl text-sm text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:border-blue-500/50 transition-all"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[10px] font-black text-zinc-500 uppercase tracking-wider" htmlFor="prescription-notes">
                    Prescription Notes
                  </label>
                  <textarea
                    id="prescription-notes"
                    value={prescriptionNotes}
                    onChange={(e) => setPrescriptionNotes(e.target.value)}
                    placeholder="e.g. Take Vitamin D daily after breakfast..."
                    rows={3}
                    className="w-full px-4 py-2.5 bg-zinc-950/50 border border-zinc-800 rounded-xl text-sm text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:border-blue-500/50 transition-all resize-none"
                  />
                </div>
              </div>

              <button 
                type="button"
                id="analyze-button"
                onClick={() => {
                  console.log("Analyze button clicked!");
                  handleUpload();
                }}
                disabled={!file || !patientId || !patientPhone || !prescriptionNotes || isProcessing}
                className="w-full mt-8 py-4 px-6 rounded-2xl bg-white text-black font-bold flex items-center justify-center gap-2 hover:bg-zinc-200 disabled:bg-zinc-800 disabled:text-zinc-500 disabled:cursor-not-allowed transition-all active:scale-[0.98] cursor-pointer relative z-50"
              >
                {isProcessing ? (
                  <div className="w-5 h-5 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                ) : (
                  <>
                    {user?.role === "intern" ? "Analyze & Submit for Co-Signature" : "Analyze Report & Start Call"}
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
                <p className="text-xs text-zinc-500 font-bold uppercase mb-1">Security</p>
                <p className="text-sm text-zinc-300">9-Layer Protected</p>
              </div>
            </div>
          </div>

          {/* Right Column: Results */}
          <div className="lg:col-span-7 min-w-0 w-full">
            <AnimatePresence mode="wait">
              {result ? (
                <motion.div 
                  key="results"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-6 min-w-0 w-full"
                >
                  <div className="p-5 sm:p-8 rounded-3xl bg-zinc-900/50 border border-zinc-800 backdrop-blur-xl w-full overflow-hidden">
                    <div className="flex items-center justify-between mb-8">
                      <h2 className="text-xl sm:text-2xl font-bold tracking-tight">Analysis Results</h2>
                      <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border ${
                        result.call_status.status === "pending_cosignature"
                          ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
                          : "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                      }`}>
                        {result.call_status.status === "pending_cosignature" ? "Queued for Co-Signature" : "Completed"}
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
                      <div className="space-y-3 w-full">
                        <h3 className="text-xs font-black text-zinc-500 uppercase tracking-[0.2em]">Patient Summary</h3>
                        <div className="p-4 sm:p-6 rounded-2xl bg-blue-500/5 border border-blue-500/10 text-zinc-300 leading-relaxed text-base sm:text-lg whitespace-pre-line break-words w-full">
                          {result.ai_summary}
                        </div>
                      </div>

                      {result.full_script && (
                        <div className="space-y-3 w-full">
                          <h3 className="text-xs font-black text-zinc-500 uppercase tracking-[0.2em]">Automated Call Transcript</h3>
                          <div className="p-4 sm:p-6 rounded-2xl bg-zinc-950/50 border border-zinc-800/50 text-zinc-400 text-xs sm:text-sm leading-relaxed font-mono whitespace-pre-line break-words w-full">
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
                        
                        {result.call_status.status !== "pending_cosignature" && result.call_status.audio_base64 && (
                          <audio 
                            controls 
                            className="h-10 rounded-full invert hue-rotate-180 brightness-150 opacity-80 hover:opacity-100 transition-opacity"
                            src={`data:audio/mp3;base64,${result.call_status.audio_base64}`}
                          />
                        )}
                        {result.call_status.status === "pending_cosignature" && (
                          <p className="text-[10px] text-yellow-400 font-bold bg-yellow-500/5 px-3 py-1.5 rounded-lg border border-yellow-500/10">
                            Simulation Paused. Waiting for Doctor's approval.
                          </p>
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

        {/* Doctor Co-Signature Queue Section */}
        {user?.role === "doctor" && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-12 p-8 rounded-3xl bg-zinc-900/50 border border-zinc-800 backdrop-blur-xl"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h2 className="text-xl font-bold flex items-center gap-2 text-zinc-100">
                  <Shield className="w-5 h-5 text-blue-400" />
                  Attending Doctor Co-Signature Queue
                </h2>
                <p className="text-xs text-zinc-500 mt-1">
                  Reports reviewed and pre-verified by Medical Interns. Approve to release outbound automated patient calls.
                </p>
              </div>

              {pendingReports.length > 0 && (
                <button
                  onClick={() => handleCosignSelected()}
                  disabled={selectedReportIds.length === 0 || isCosigning}
                  className="px-6 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 disabled:bg-zinc-800 disabled:text-zinc-650 text-black font-bold text-xs transition-all flex items-center gap-2 cursor-pointer active:scale-[0.98]"
                >
                  {isCosigning ? (
                    <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                  ) : (
                    <>
                      Co-Sign & Call ({selectedReportIds.length})
                    </>
                  )}
                </button>
              )}
            </div>

            {pendingReports.length === 0 ? (
              <div className="text-center py-12 border border-dashed border-zinc-855 rounded-2xl bg-zinc-950/20">
                <p className="text-zinc-500 text-sm">No reports pending doctor co-signature.</p>
              </div>
            ) : (
              <div className="overflow-x-auto rounded-2xl border border-zinc-800 bg-zinc-950/30">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-zinc-800 text-[10px] text-zinc-500 uppercase tracking-widest font-black bg-zinc-900/30">
                      <th className="p-4 w-12 text-center">
                        <input
                          type="checkbox"
                          className="w-4 h-4 accent-emerald-500 rounded border-zinc-700 bg-zinc-950 cursor-pointer"
                          checked={selectedReportIds.length === pendingReports.length}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setSelectedReportIds(pendingReports.map(r => r.report_id));
                            } else {
                              setSelectedReportIds([]);
                            }
                          }}
                        />
                      </th>
                      <th className="p-4">Patient ID</th>
                      <th className="p-4">Phone Number</th>
                      <th className="p-4">Hemoglobin</th>
                      <th className="p-4">Cholesterol</th>
                      <th className="p-4">Vitamin D3</th>
                      <th className="p-4">Prescription Notes</th>
                      <th className="p-4 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {pendingReports.map((report) => (
                      <tr key={report.report_id} className="border-b border-zinc-800/80 hover:bg-zinc-900/20 transition-colors">
                        <td className="p-4 text-center">
                          <input
                            type="checkbox"
                            className="w-4 h-4 accent-emerald-500 rounded border-zinc-700 bg-zinc-950 cursor-pointer"
                            checked={selectedReportIds.includes(report.report_id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedReportIds([...selectedReportIds, report.report_id]);
                              } else {
                                setSelectedReportIds(selectedReportIds.filter(id => id !== report.report_id));
                              }
                            }}
                          />
                        </td>
                        <td className="p-4 font-mono text-xs text-zinc-300 font-bold">{report.patient_id.substring(0, 8)}...</td>
                        <td className="p-4 text-xs text-zinc-400">{report.patient_phone}</td>
                        <td className="p-4 text-xs font-mono">{report.hemoglobin ?? "—"}</td>
                        <td className="p-4 text-xs font-mono">{report.cholesterol ?? "—"}</td>
                        <td className="p-4 text-xs font-mono">{report.vitamin_d ?? "—"}</td>
                        <td className="p-4 text-xs text-zinc-400 max-w-[200px] truncate" title={report.prescription_notes}>
                          {report.prescription_notes}
                        </td>
                        <td className="p-4 text-right">
                          <button
                            onClick={() => {
                              handleCosignSelected([report.report_id]);
                            }}
                            className="px-3 py-1 rounded bg-zinc-900 border border-zinc-800 hover:border-emerald-500/30 text-emerald-400 text-[10px] font-bold uppercase transition-all"
                          >
                            Approve
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </motion.div>
        )}

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
