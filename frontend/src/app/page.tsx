'use client';

import React, { useState } from 'react';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('patient_id', 'p' + Math.floor(Math.random() * 1000));
    formData.append('patient_phone_number', '+1234567890');

    try {
      const res = await fetch(`${API_URL}/api/v1/reports/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error('Upload failed:', err);
      alert('Upload failed. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0b] text-zinc-100 p-8 font-sans">
      <header className="max-w-6xl mx-auto mb-16 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            MediAssist AI
          </h1>
          <p className="mt-2 text-zinc-500">Free Automated Patient Follow-up System</p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Upload Section */}
        <section className="lg:col-span-5 space-y-6">
          <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-8 shadow-2xl backdrop-blur-sm">
            <h2 className="text-xl font-semibold mb-6">Upload Lab Report</h2>
            <form onSubmit={handleUpload} className="space-y-4">
              <div className="relative group">
                <input
                  type="file"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="hidden"
                  id="file-upload"
                  accept=".pdf"
                />
                <label
                  htmlFor="file-upload"
                  className="flex flex-col items-center justify-center w-full h-48 border-2 border-dashed border-zinc-700 rounded-xl cursor-pointer hover:border-emerald-500/50 hover:bg-emerald-500/5 transition-all"
                >
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <svg className="w-10 h-10 mb-3 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="mb-2 text-sm text-zinc-400">
                      <span className="font-semibold">{file ? file.name : "Click to upload"}</span>
                    </p>
                    <p className="text-xs text-zinc-500">PDF (MAX. 10MB)</p>
                  </div>
                </label>
              </div>

              <button
                type="submit"
                disabled={!file || loading}
                className="w-full py-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed font-bold text-white shadow-lg shadow-emerald-900/20 transition-all flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Processing...
                  </>
                ) : "Analyze Report & Start Call"}
              </button>
            </form>
          </div>
        </section>

        {/* Results Section */}
        <section className="lg:col-span-7">
          {result ? (
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-8 shadow-2xl backdrop-blur-sm animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl font-bold">Analysis Results</h2>
                <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-bold rounded-full uppercase tracking-widest border border-emerald-500/20">
                  Completed
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
                {Object.entries(result.extracted_data || {}).map(([key, val]: any) => (
                  <div key={key} className="p-4 rounded-xl bg-zinc-800/50 border border-zinc-700/50">
                    <p className="text-xs text-zinc-500 uppercase font-bold tracking-tight">{key}</p>
                    <p className="text-2xl font-mono text-emerald-400">{val}</p>
                  </div>
                ))}
              </div>

              <div className="space-y-4">
                <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-widest">AI Patient Summary</h3>
                <div className="p-6 rounded-xl bg-blue-500/5 border border-blue-500/20 text-zinc-200 leading-relaxed italic">
                  "{result.ai_summary}"
                </div>
              </div>

              <div className="mt-8 pt-8 border-t border-zinc-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-center gap-4 text-sm text-zinc-500">
                  <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                  {result.call_status.message}
                </div>
                
                {result.call_status.audio_file && (
                  <div className="flex flex-col gap-2">
                    <p className="text-[10px] text-zinc-600 uppercase font-bold text-right mr-2">Simulated Call Audio</p>
                    <audio 
                      controls 
                      className="h-10 rounded-lg bg-zinc-800"
                      src={`${API_URL}/temp_calls/${result.call_status.audio_file}`}
                    >
                      Your browser does not support the audio element.
                    </audio>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center border border-dashed border-zinc-800 rounded-2xl p-12 text-zinc-600">
              Upload a report to see the AI analysis here.
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
