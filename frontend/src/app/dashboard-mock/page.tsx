'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  UserCircle,
  FileText,
  Settings,
  ShieldCheck,
  Languages,
  Zap
} from 'lucide-react';
import { cn } from '@/lib/utils';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [lang, setLang] = useState('ar');
  const [isRTL, setIsRTL] = useState(true);

  useEffect(() => {
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;
  }, [isRTL, lang]);

  const toggleLang = () => {
    setLang(lang === 'ar' ? 'en' : 'ar');
    setIsRTL(!isRTL);
  };

  const menuItems = [
    { icon: LayoutDashboard, label: lang === 'ar' ? 'لوحة التحكم' : 'Dashboard' },
    { icon: UserCircle, label: lang === 'ar' ? 'الملف الشخصي' : 'Profile' },
    { icon: FileText, label: lang === 'ar' ? 'مولد العروض' : 'Proposal Gen' },
    { icon: ShieldCheck, label: lang === 'ar' ? 'الاختبار الذكي' : 'Smart Quiz' },
    { icon: Settings, label: lang === 'ar' ? 'الإعدادات' : 'Settings' },
  ];

  return (
    <div className="min-h-screen bg-bg-snow flex flex-col md:flex-row">
      {/* Sidebar */}
      <aside className={cn(
        "w-full md:w-64 bg-white border-muted-slate/10 border-e shadow-sm flex flex-col",
        isRTL ? "md:right-0" : "md:left-0"
      )}>
        <div className="p-6 flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shadow-lg shadow-primary/20">
            <Zap size={24} />
          </div>
          <span className="text-xl font-bold text-text-dark tracking-tight">VeriPitch</span>
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          {menuItems.map((item, idx) => (
            <button
              key={idx}
              className={cn(
                "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200",
                idx === 0
                  ? "bg-primary/10 text-primary font-medium"
                  : "text-muted-slate hover:bg-bg-snow hover:text-text-dark"
              )}
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-muted-slate/10">
          <button
            onClick={toggleLang}
            className="w-full flex items-center justify-between px-4 py-2 text-sm text-muted-slate hover:text-primary transition-colors"
          >
            <div className="flex items-center gap-2">
              <Languages size={18} />
              <span>{lang === 'ar' ? 'English' : 'العربية'}</span>
            </div>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-4 md:p-8 overflow-y-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-text-dark">
              {lang === 'ar' ? 'أهلاً بك، فريلانسر!' : 'Welcome, Freelancer!'}
            </h1>
            <p className="text-muted-slate mt-1">
              {lang === 'ar' ? 'جاهز لصناعة عرض عمل احترافي؟' : 'Ready to craft a professional proposal?'}
            </p>
          </div>
          <div className="flex items-center gap-4">
             <div className="bg-white p-2 rounded-full shadow-sm border border-muted-slate/10">
                <div className="w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold">
                  JS
                </div>
             </div>
          </div>
        </header>

        {children}
        <div className="space-y-8">
          <ProfileBuilder />
          <ProposalGenerator />
        </div>
      </main>
    </div>
  );
}

import ProposalGenerator from './ProposalGenerator';
import ProfileBuilder from './ProfileBuilder';
