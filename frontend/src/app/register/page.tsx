"use client";

import { Suspense } from "react";
import AuthCard from "@/components/AuthCard";

export default function RegisterPage() {
  return (
    <Suspense fallback={
      <main className="min-h-screen bg-[#09090b] text-zinc-100 flex items-center justify-center">
        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
      </main>
    }>
      <AuthCard initialMode="register" />
    </Suspense>
  );
}
