"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { LogIn, UserPlus, Mail, Lock, User, AlertCircle, ArrowLeft, ArrowRight, Eye, EyeOff } from "lucide-react";
import { login, register } from "@/lib/auth";
import { useRouter, useSearchParams } from "next/navigation";

interface AuthCardProps {
  initialMode: "login" | "register";
}

export default function AuthCard({ initialMode }: AuthCardProps) {
  const [mode, setMode] = useState<"login" | "register">(initialMode);
  
  // Login form state
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [showLoginPassword, setShowLoginPassword] = useState(false);
  const [loginError, setLoginError] = useState("");
  const [isLoginLoading, setIsLoginLoading] = useState(false);

  // Register form state
  const [regFullName, setRegFullName] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [showRegPassword, setShowRegPassword] = useState(false);
  const [regRole, setRegRole] = useState("patient");
  const [regError, setRegError] = useState("");
  const [isRegLoading, setIsRegLoading] = useState(false);

  const router = useRouter();
  const searchParams = useSearchParams();

  // Sync mode with browser back/forward buttons
  useEffect(() => {
    const handlePopState = () => {
      const path = window.location.pathname;
      if (path === "/register") {
        setMode("register");
      } else if (path === "/login") {
        setMode("login");
      }
    };

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  // Check if we just redirected after registration
  useEffect(() => {
    if (searchParams?.get("registered") === "true") {
      setLoginError("");
    }
  }, [searchParams]);

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError("");
    setIsLoginLoading(true);

    try {
      await login(loginEmail, loginPassword);
      router.push("/");
    } catch (err: any) {
      setLoginError(err.message || "Login failed. Please check your credentials.");
    } finally {
      setIsLoginLoading(false);
    }
  };

  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setRegError("");

    if (regPassword.length < 8) {
      setRegError("Password must be at least 8 characters long.");
      return;
    }

    setIsRegLoading(true);

    try {
      await register(regEmail, regPassword, regFullName, regRole);
      // Instead of full page redirect, switch view state to login
      setLoginEmail(regEmail);
      setMode("login");
      window.history.pushState(null, "", "/login?registered=true");
      setLoginError(""); // Clear any previous login errors
    } catch (err: any) {
      setRegError(err.message || "Registration failed. Please try again.");
    } finally {
      setIsRegLoading(false);
    }
  };

  const navigateToRegister = () => {
    setMode("register");
    window.history.pushState(null, "", "/register");
    setRegError("");
  };

  const navigateToLogin = () => {
    setMode("login");
    window.history.pushState(null, "", "/login");
    setLoginError("");
  };

  // Only patient and staff roles are available for self-registration.
  // Doctor, intern, and admin accounts must be created by an admin.
  const roles = [
    { value: "patient", label: "Patient", description: "Personal access" },
    { value: "staff", label: "Staff", description: "General access" },
  ];

  return (
    <main className="min-h-screen bg-[#09090b] text-zinc-100 flex items-center justify-center relative overflow-hidden">
      {/* Background Glow */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] bg-blue-600/8 blur-[150px] rounded-full" />
        <div className="absolute bottom-[10%] -right-[10%] w-[40%] h-[40%] bg-emerald-600/8 blur-[150px] rounded-full" />
      </div>

      <div className="w-full max-w-md mx-4 relative z-10">
        <AnimatePresence mode="wait">
          {mode === "login" ? (
            <motion.div
              key="login"
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 30 }}
              transition={{ duration: 0.3, ease: "easeInOut" }}
            >
              {/* Header */}
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent">
                  Welcome Back
                </h1>
                <p className="text-zinc-500 mt-2">Sign in to your MediAssist account</p>
              </div>

              {/* Login Form */}
              <div className="p-8 rounded-3xl bg-zinc-900/50 border border-zinc-800 backdrop-blur-xl">
                <form onSubmit={handleLoginSubmit} className="space-y-5">
                  {/* Success Message from Register Redirect */}
                  {(searchParams?.get("registered") === "true" || loginEmail) && !loginError && (
                    <div className="flex items-center gap-2 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm">
                      Registration successful! Please sign in.
                    </div>
                  )}

                  {/* Error Message */}
                  {loginError && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="flex items-center gap-2 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm"
                    >
                      <AlertCircle className="w-4 h-4 shrink-0" />
                      {loginError}
                    </motion.div>
                  )}

                  {/* Email */}
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 uppercase tracking-wider" htmlFor="login-email">
                      Email
                    </label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                      <input
                        id="login-email"
                        type="email"
                        value={loginEmail}
                        onChange={(e) => setLoginEmail(e.target.value)}
                        placeholder="doctor@clinic.com"
                        required
                        className="w-full pl-10 pr-4 py-3 bg-zinc-950/50 border border-zinc-800 rounded-xl text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all"
                      />
                    </div>
                  </div>

                  {/* Password */}
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 uppercase tracking-wider" htmlFor="login-password">
                      Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                      <input
                        id="login-password"
                        type={showLoginPassword ? "text" : "password"}
                        value={loginPassword}
                        onChange={(e) => setLoginPassword(e.target.value)}
                        placeholder="Enter your password"
                        required
                        className="w-full pl-10 pr-10 py-3 bg-zinc-950/50 border border-zinc-800 rounded-xl text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all"
                      />
                      <button
                        type="button"
                        onClick={() => setShowLoginPassword(!showLoginPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500 hover:text-zinc-300 transition-colors focus:outline-none"
                      >
                        {showLoginPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  {/* Submit */}
                  <button
                    type="submit"
                    disabled={isLoginLoading}
                    className="w-full py-3.5 px-6 rounded-xl bg-white text-black font-bold flex items-center justify-center gap-2 hover:bg-zinc-200 disabled:bg-zinc-800 disabled:text-zinc-500 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
                  >
                    {isLoginLoading ? (
                      <div className="w-5 h-5 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                    ) : (
                      <>
                        <LogIn className="w-4 h-4" />
                        Sign In
                      </>
                    )}
                  </button>
                </form>

                {/* Divider */}
                <div className="flex items-center gap-3 my-6">
                  <div className="flex-1 h-px bg-zinc-800" />
                  <span className="text-xs text-zinc-600 font-bold uppercase">or</span>
                  <div className="flex-1 h-px bg-zinc-800" />
                </div>

                {/* Register Trigger */}
                <button
                  onClick={navigateToRegister}
                  className="w-full py-3 px-6 rounded-xl border border-zinc-800 text-zinc-400 font-semibold flex items-center justify-center gap-2 hover:bg-zinc-800/50 hover:text-zinc-200 transition-all"
                >
                  Create an Account
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="register"
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -30 }}
              transition={{ duration: 0.3, ease: "easeInOut" }}
            >
              {/* Back Link */}
              <button
                onClick={navigateToLogin}
                className="inline-flex items-center gap-1 text-zinc-500 hover:text-zinc-300 text-sm mb-6 transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                Back to Login
              </button>

              {/* Header */}
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent">
                  Create Account
                </h1>
                <p className="text-zinc-500 mt-2">Join MediAssist AI platform</p>
              </div>

              {/* Register Form */}
              <div className="p-8 rounded-3xl bg-zinc-900/50 border border-zinc-800 backdrop-blur-xl">
                <form onSubmit={handleRegisterSubmit} className="space-y-5">
                  {/* Error Message */}
                  {regError && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="flex items-center gap-2 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm"
                    >
                      <AlertCircle className="w-4 h-4 shrink-0" />
                      {regError}
                    </motion.div>
                  )}

                  {/* Full Name */}
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 uppercase tracking-wider" htmlFor="reg-name">
                      Full Name
                    </label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                      <input
                        id="reg-name"
                        type="text"
                        value={regFullName}
                        onChange={(e) => setRegFullName(e.target.value)}
                        placeholder="Dr. Jane Smith"
                        required
                        className="w-full pl-10 pr-4 py-3 bg-zinc-950/50 border border-zinc-800 rounded-xl text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/20 transition-all"
                      />
                    </div>
                  </div>

                  {/* Email */}
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 uppercase tracking-wider" htmlFor="reg-email">
                      Email
                    </label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                      <input
                        id="reg-email"
                        type="email"
                        value={regEmail}
                        onChange={(e) => setRegEmail(e.target.value)}
                        placeholder="doctor@clinic.com"
                        required
                        className="w-full pl-10 pr-4 py-3 bg-zinc-950/50 border border-zinc-800 rounded-xl text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/20 transition-all"
                      />
                    </div>
                  </div>

                  {/* Password */}
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 uppercase tracking-wider" htmlFor="reg-password">
                      Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                      <input
                        id="reg-password"
                        type={showRegPassword ? "text" : "password"}
                        value={regPassword}
                        onChange={(e) => setRegPassword(e.target.value)}
                        placeholder="Min. 8 characters"
                        required
                        minLength={8}
                        className="w-full pl-10 pr-10 py-3 bg-zinc-950/50 border border-zinc-800 rounded-xl text-zinc-200 placeholder:text-zinc-600 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/20 transition-all"
                      />
                      <button
                        type="button"
                        onClick={() => setShowRegPassword(!showRegPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500 hover:text-zinc-300 transition-colors focus:outline-none"
                      >
                        {showRegPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  {/* Role Selection */}
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 uppercase tracking-wider">
                      Role
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      {roles.map((r, index) => (
                        <button
                          key={r.value}
                          type="button"
                          onClick={() => setRegRole(r.value)}
                          className={`p-3 rounded-xl border text-center transition-all ${
                            regRole === r.value
                              ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-400"
                              : "border-zinc-800 bg-zinc-950/50 text-zinc-500 hover:border-zinc-700"
                          }`}
                        >
                          <p className="text-sm font-bold">{r.label}</p>
                          <p className="text-[10px] mt-0.5 opacity-60">{r.description}</p>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Submit */}
                  <button
                    type="submit"
                    disabled={isRegLoading}
                    className="w-full py-3.5 px-6 rounded-xl bg-white text-black font-bold flex items-center justify-center gap-2 hover:bg-zinc-200 disabled:bg-zinc-800 disabled:text-zinc-500 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
                  >
                    {isRegLoading ? (
                      <div className="w-5 h-5 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                    ) : (
                      <>
                        <UserPlus className="w-4 h-4" />
                        Create Account
                      </>
                    )}
                  </button>
                </form>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        <p className="text-center mt-6 text-zinc-600 text-xs uppercase tracking-widest font-bold">
          MediAssist AI &bull; Secure Healthcare
        </p>
      </div>
    </main>
  );
}
