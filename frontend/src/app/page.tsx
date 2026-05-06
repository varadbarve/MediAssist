import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-background p-8">
      <header className="mb-12 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold tracking-tight text-foreground">MediAssist AI</h1>
          <p className="mt-2 text-zinc-500">Automated Patient Follow-up & Report Explanation</p>
        </div>
        <div className="flex gap-4">
          <button className="rounded-lg bg-primary px-4 py-2 font-medium text-primary-foreground transition-all hover:opacity-90">
            Upload Report
          </button>
          <button className="rounded-lg border border-border bg-card px-4 py-2 font-medium transition-all hover:bg-accent">
            Settings
          </button>
        </div>
      </header>

      <main className="grid grid-cols-1 gap-8 md:grid-cols-3">
        {/* Status Overview */}
        <section className="col-span-1 space-y-6 md:col-span-2">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
              <h3 className="text-sm font-medium text-zinc-500">Total Calls Today</h3>
              <p className="mt-2 text-3xl font-bold">124</p>
              <div className="mt-2 flex items-center text-xs text-green-500">
                <span>↑ 12% from yesterday</span>
              </div>
            </div>
            <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
              <h3 className="text-sm font-medium text-zinc-500">Successful Explanations</h3>
              <p className="mt-2 text-3xl font-bold">92%</p>
              <div className="mt-2 flex items-center text-xs text-green-500">
                <span>↑ 3% from average</span>
              </div>
            </div>
            <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
              <h3 className="text-sm font-medium text-zinc-500">Pending Escalations</h3>
              <p className="mt-2 text-3xl font-bold">5</p>
              <div className="mt-2 flex items-center text-xs text-red-500">
                <span>Critical attention required</span>
              </div>
            </div>
            <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
              <h3 className="text-sm font-medium text-zinc-500">Reports Processed</h3>
              <p className="mt-2 text-3xl font-bold">1,042</p>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="rounded-xl border border-border bg-card shadow-sm">
            <div className="border-b border-border p-6">
              <h2 className="text-xl font-bold">Recent Patient Interactions</h2>
            </div>
            <div className="p-6">
              <table className="w-full text-left">
                <thead>
                  <tr className="text-xs font-medium uppercase text-zinc-500">
                    <th className="pb-4">Patient</th>
                    <th className="pb-4">Status</th>
                    <th className="pb-4">Action</th>
                    <th className="pb-4 text-right">Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {[
                    { name: 'John Doe', status: 'Call Completed', action: 'Summary Delivered', time: '10 mins ago' },
                    { name: 'Jane Smith', status: 'In Progress', action: 'Asking Questions', time: '2 mins ago' },
                    { name: 'Robert Brown', status: 'Escalated', action: 'Needs Doctor Call', time: '1 hour ago' },
                    { name: 'Alice Wilson', status: 'Pending', action: 'Report Uploaded', time: 'Just now' },
                  ].map((item, i) => (
                    <tr key={i} className="text-sm">
                      <td className="py-4 font-medium">{item.name}</td>
                      <td className="py-4">
                        <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${
                          item.status === 'Call Completed' ? 'bg-green-100 text-green-700' :
                          item.status === 'Escalated' ? 'bg-red-100 text-red-700' :
                          'bg-blue-100 text-blue-700'
                        }`}>
                          {item.status}
                        </span>
                      </td>
                      <td className="py-4 text-zinc-500">{item.action}</td>
                      <td className="py-4 text-right text-zinc-500">{item.time}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Sidebar/Quick Actions */}
        <section className="col-span-1 space-y-6">
          <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
            <h2 className="mb-4 text-lg font-bold">System Status</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm">Twilio Voice API</span>
                <span className="h-2 w-2 rounded-full bg-green-500"></span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">OpenAI LLM</span>
                <span className="h-2 w-2 rounded-full bg-green-500"></span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">ElevenLabs TTS</span>
                <span className="h-2 w-2 rounded-full bg-green-500"></span>
              </div>
            </div>
          </div>

          <div className="rounded-xl bg-gradient-to-br from-primary to-blue-600 p-6 text-white shadow-lg">
            <h2 className="mb-2 text-lg font-bold">New Feature</h2>
            <p className="text-sm opacity-90">Multi-language support is now available for patient summaries. Check settings to enable.</p>
            <button className="mt-4 rounded-lg bg-white px-4 py-2 text-sm font-medium text-primary hover:bg-zinc-100">
              Learn More
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}
