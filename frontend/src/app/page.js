'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, Rocket, Zap, ChevronLeft } from 'lucide-react';

export default function LoginPage() {
  const WHOP_APP_ID = process.env.NEXT_PUBLIC_WHOP_APP_ID;

  const getRedirectUri = () => {
    if (typeof window !== 'undefined') {
      return `${window.location.origin}/api/auth/whop`;
    }
    return "http://localhost:3000/api/auth/whop";
  };

  const REDIRECT_URL = getRedirectUri();

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white flex flex-col items-center justify-center relative overflow-hidden font-sans">
      {/* Background Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-red-900/20 rounded-full blur-[120px]" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-900/20 rounded-full blur-[120px]" />

      <main className="relative z-10 container mx-auto px-6 flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mb-8"
        >
          <div className="inline-flex items-center space-x-2 space-x-reverse bg-white/5 border border-white/10 px-4 py-2 rounded-full mb-6">
            <Zap className="w-4 h-4 text-red-500 fill-red-500" />
            <span className="text-sm font-medium">مرحباً بك في مستقبل العمل الحر</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight">
            عروض عمل <span className="bg-gradient-to-l from-red-500 to-red-300 bg-clip-text text-transparent">صادقة</span> واحترافية
          </h1>

          <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed mb-10">
            VeriPitch تضمن لك صياغة عروض عمل مقنعة ومبنية 100% على مهاراتك الحقيقية، بعيداً عن هلوسة الذكاء الاصطناعي.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="flex flex-col items-center"
        >
          <a
            href={`https://whop.com/oauth/authorize?client_id=${WHOP_APP_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URL)}&response_type=code&scope=user_profile%20memberships`}
            className="group relative inline-flex items-center justify-center px-10 py-4 font-bold text-white transition-all duration-200 bg-red-600 font-pj rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
          >
            <span className="relative inline-flex items-center">
              سجل دخولك عبر Whop
              <ChevronLeft className="mr-2 w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            </span>
          </a>

          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-4xl text-right">
            <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
              <ShieldCheck className="w-8 h-8 text-red-500 mb-4" />
              <h3 className="font-bold text-lg mb-2">صدق بنسبة 100%</h3>
              <p className="text-gray-400 text-sm">نحن لا نختلق مهارات وهمية، بل نبرز قوتك الحقيقية.</p>
            </div>
            <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
              <Zap className="w-8 h-8 text-blue-500 mb-4" />
              <h3 className="font-bold text-lg mb-2">سرعة فائقة</h3>
              <p className="text-gray-400 text-sm">حلل متطلبات الوظيفة وصيغ عرضك في ثوانٍ معدودة.</p>
            </div>
            <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
              <Rocket className="w-8 h-8 text-purple-500 mb-4" />
              <h3 className="font-bold text-lg mb-2">نمو مهني</h3>
              <p className="text-gray-400 text-sm">اكتشف الفجوات المهارية واحصل على توجيه لتعلمها.</p>
            </div>
          </div>
        </motion.div>
      </main>

      <footer className="absolute bottom-10 text-gray-500 text-sm">
        &copy; 2026 VeriPitch. جميع الحقوق محفوظة.
      </footer>
    </div>
  );
}
