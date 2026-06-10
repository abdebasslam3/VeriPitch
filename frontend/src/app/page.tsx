'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Zap, ShieldCheck, Sparkles, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function LandingPage() {
  const WHOP_AUTH_URL = `https://whop.com/oauth?client_id=${process.env.NEXT_PUBLIC_WHOP_CLIENT_ID}&redirect_uri=${encodeURIComponent(process.env.NEXT_PUBLIC_WHOP_REDIRECT_URI || '')}&response_type=code`;

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-[#0F172A] font-sans selection:bg-primary selection:text-white">
      {/* Navigation */}
      <nav className="flex items-center justify-between px-6 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-[#1DA1F2] rounded-xl flex items-center justify-center text-white shadow-lg shadow-[#1DA1F2]/20">
            <Zap size={24} />
          </div>
          <span className="text-2xl font-bold tracking-tight">VeriPitch</span>
        </div>
        <a
          href={WHOP_AUTH_URL}
          className="bg-white border border-[#64748B]/10 px-6 py-2 rounded-full font-medium hover:bg-white/80 transition-all shadow-sm"
        >
          تسجيل الدخول
        </a>
      </nav>

      {/* Hero Section */}
      <header className="max-w-7xl mx-auto px-6 pt-20 pb-32 text-center md:text-right flex flex-col md:flex-row-reverse items-center justify-between gap-12">
        <div className="md:w-1/2 space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 bg-[#1DA1F2]/10 text-[#1DA1F2] px-4 py-2 rounded-full text-sm font-bold"
          >
            <Sparkles size={16} /> مدعوم بالذكاء الاصطناعي الصادق
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-5xl md:text-7xl font-black leading-[1.1] text-[#0F172A]"
          >
            حول خبرتك الحقيقية إلى <span className="text-[#1DA1F2]">عروض عمل</span> لا تُرفض
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl text-[#64748B] max-w-xl md:ms-auto"
          >
            أول منصة للفريلانسرز تضمن صياغة عروض عمل (Proposals) صادقة 100%، موثقة، وخالية من الهلوسة بناءً على مهاراتك الفعلية فقط.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="pt-6"
          >
            <a
              href={WHOP_AUTH_URL}
              className="bg-[#1DA1F2] text-white px-10 py-5 rounded-2xl font-bold text-lg flex items-center justify-center gap-3 hover:bg-[#1DA1F2]/90 transition-all shadow-xl shadow-[#1DA1F2]/20 md:inline-flex w-full md:w-auto"
            >
              ابدأ الآن مجاناً عبر Whop <ArrowRight size={20} />
            </a>
          </motion.div>
        </div>

        <motion.div
           initial={{ opacity: 0, scale: 0.9 }}
           animate={{ opacity: 1, scale: 1 }}
           transition={{ delay: 0.4 }}
           className="md:w-1/2 bg-white p-4 rounded-[2.5rem] shadow-2xl border border-[#64748B]/5 rotate-2"
        >
          <div className="bg-[#F8FAFC] rounded-[2rem] p-8 aspect-square flex items-center justify-center border border-[#64748B]/5 overflow-hidden">
             <div className="space-y-4 w-full">
                <div className="h-4 w-3/4 bg-slate-200 rounded-full animate-pulse" />
                <div className="h-4 w-1/2 bg-slate-200 rounded-full animate-pulse" />
                <div className="h-32 w-full bg-[#1DA1F2]/5 rounded-2xl border-2 border-dashed border-[#1DA1F2]/20 flex items-center justify-center text-[#1DA1F2]">
                   <ShieldCheck size={48} />
                </div>
                <div className="h-4 w-full bg-slate-200 rounded-full animate-pulse" />
             </div>
          </div>
        </motion.div>
      </header>

      {/* Features */}
      <section className="bg-white py-32 border-t border-[#64748B]/5">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-12">
          {[
            { icon: ShieldCheck, title: "الصدق الرقمي", desc: "نستخدم تقنية RAG لضمان أن كل عرض عمل يعتمد فقط على ما هو موجود فعلياً في ملفك الشخصي." },
            { icon: Zap, title: "سرعة البرق", desc: "حول وصف الوظيفة المعقد إلى عرض عمل مخصص في أقل من 30 ثانية باستخدام Gemini و Claude." },
            { icon: Sparkles, title: "سد الفجوة المعرفية", desc: "نظام اختبارات ذكي يكتشف مهاراتك الناقصة ويقترح عليك مصادر لتعلمها وتوثيقها." }
          ].map((feature, i) => (
            <div key={i} className="text-center md:text-right space-y-4">
              <div className="w-16 h-16 bg-[#1DA1F2]/10 text-[#1DA1F2] rounded-2xl flex items-center justify-center mx-auto md:ms-auto">
                <feature.icon size={32} />
              </div>
              <h3 className="text-2xl font-bold text-[#0F172A]">{feature.title}</h3>
              <p className="text-[#64748B] leading-relaxed">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-[#64748B]/5 text-center text-[#64748B] text-sm">
        © 2024 VeriPitch - منصة العمل الحر المستقبلية. جميع الحقوق محفوظة.
      </footer>
    </div>
  );
}
