'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Copy, Check, Sparkles, BrainCircuit } from 'lucide-react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function ProposalGenerator() {
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [proposal, setProposal] = useState('');
  const [copied, setCopied] = useState(false);
  const [score, setScore] = useState(85);

  const handleGenerate = async () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setProposal("تم توليد عرض العمل بناءً على مهاراتك الموثقة في React و Node.js...");
      setLoading(false);
    }, 2000);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(proposal);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const chartData = {
    datasets: [{
      data: [score, 100 - score],
      backgroundColor: ['#1DA1F2', '#E2E8F0'],
      borderWidth: 0,
      circumference: 180,
      rotation: 270,
    }]
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Input Section */}
      <div className="lg:col-span-2 space-y-6">
        <section className="bg-white p-6 rounded-2xl shadow-sm border border-muted-slate/10">
          <label className="block text-lg font-bold text-text-dark mb-4">وصف الوظيفة</label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            className="w-full h-48 p-4 bg-bg-snow border border-muted-slate/20 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all resize-none"
            placeholder="انسخ وصف الوظيفة هنا..."
          />
          <div className="mt-4 flex gap-4">
             <button
              onClick={handleGenerate}
              disabled={loading || !jobDescription}
              className="flex-1 bg-primary text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-primary/90 transition-all disabled:opacity-50"
            >
              {loading ? <Sparkles className="animate-spin" /> : <Send size={20} />}
              توليد العرض الآن
            </button>
          </div>
        </section>

        {proposal && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white p-6 rounded-2xl shadow-sm border border-muted-slate/10 relative"
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-text-dark flex items-center gap-2">
                <BrainCircuit className="text-primary" /> العرض المقترح
              </h3>
              <button
                onClick={copyToClipboard}
                className="p-2 hover:bg-bg-snow rounded-lg transition-colors flex items-center gap-2 text-sm text-primary"
              >
                {copied ? <Check size={18} /> : <Copy size={18} />}
                {copied ? 'تم النسخ' : 'نسخ النص'}
              </button>
            </div>
            <div className="prose max-w-none text-text-dark whitespace-pre-wrap leading-relaxed">
              {proposal}
            </div>
          </motion.section>
        )}
      </div>

      {/* Sidebar Stats */}
      <div className="space-y-6">
        <section className="bg-white p-6 rounded-2xl shadow-sm border border-muted-slate/10 text-center">
          <h3 className="font-bold text-text-dark mb-4">Market Fit Score</h3>
          <div className="w-48 h-24 mx-auto relative">
            <Doughnut data={chartData} options={{ cutout: '80%', plugins: { tooltip: { enabled: false } } }} />
            <div className="absolute inset-0 flex items-end justify-center pb-2">
              <span className="text-3xl font-bold text-primary">{score}%</span>
            </div>
          </div>
          <p className="text-sm text-muted-slate mt-4">
            مهاراتك تطابق متطلبات الوظيفة بنسبة عالية!
          </p>
        </section>

        <section className="bg-accent-coral/5 p-6 rounded-2xl border border-accent-coral/10">
          <h4 className="text-accent-coral font-bold flex items-center gap-2 mb-2">
            <Sparkles size={18} /> فجوة معرفية مكتشفة
          </h4>
          <p className="text-sm text-muted-slate mb-4">
            تتطلب الوظيفة مهارة <span className="font-bold text-text-dark">GraphQL</span>. هل تود توثيقها الآن؟
          </p>
          <button className="w-full py-2 bg-accent-coral text-white rounded-lg font-medium hover:bg-accent-coral/90 transition-colors">
            بدء الاختبار الذكي
          </button>
        </section>
      </div>
    </div>
  );
}
