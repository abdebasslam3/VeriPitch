'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Copy, Check, Sparkles, BrainCircuit, AlertCircle } from 'lucide-react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { encryptApiKey } from '@/lib/encryption';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function ProposalGenerator() {
  const [jobDescription, setJobDescription] = useState('');
  const [screeningQuestions, setScreeningQuestions] = useState('');
  const [modelChoice, setModelChoice] = useState('gemini');
  const [loading, setLoading] = useState(false);
  const [proposal, setProposal] = useState('');
  const [copied, setCopied] = useState(false);
  const [score, setScore] = useState<number | null>(null);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    setLoading(true);
    setError('');

    // Retrieve credentials from localStorage (Zero-Knowledge)
    const apiKeyRaw = localStorage.getItem(`${modelChoice.toUpperCase()}_API_KEY`);
    const dynamicSalt = sessionStorage.getItem('DYNAMIC_SALT');
    const whopUserId = sessionStorage.getItem('WHOP_USER_ID');

    if (!apiKeyRaw || !dynamicSalt || !whopUserId) {
      setError('يرجى ضبط مفاتيح الـ API في الإعدادات أولاً');
      setLoading(false);
      return;
    }

    try {
      // 1. Encrypt API key in browser
      const encryptedKey = encryptApiKey(apiKeyRaw, dynamicSalt);

      // 2. Prepare Form Data
      const formData = new FormData();
      formData.append('whop_user_id', whopUserId);
      formData.append('job_description', jobDescription);
      formData.append('screening_questions', screeningQuestions);
      formData.append('model_choice', modelChoice);
      formData.append('encrypted_api_key', encryptedKey);
      formData.append('dynamic_salt', dynamicSalt);

      const response = await fetch('/api/v1/generate-proposal', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setProposal(data.proposal);
        setScore(data.market_fit_score);
      } else {
        setError(data.detail || 'فشل في توليد العرض');
      }
    } catch (err) {
      setError('حدث خطأ أثناء الاتصال بالسيرفر');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(proposal);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const chartData = {
    datasets: [{
      data: [score || 0, 100 - (score || 0)],
      backgroundColor: ['#1DA1F2', '#E2E8F0'],
      borderWidth: 0,
      circumference: 180,
      rotation: 270,
    }]
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2 space-y-6">
        <section className="bg-white p-6 rounded-2xl shadow-sm border border-muted-slate/10">
          <div className="flex justify-between items-center mb-4">
            <label className="text-lg font-bold text-text-dark">وصف الوظيفة</label>
            <select
              value={modelChoice}
              onChange={(e) => setModelChoice(e.target.value)}
              className="bg-bg-snow p-2 rounded-lg border border-muted-slate/10 text-sm outline-none"
            >
              <option value="gemini">Gemini 1.5 Flash</option>
              <option value="claude">Claude 3.5 Sonnet</option>
            </select>
          </div>

          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            className="w-full h-48 p-4 bg-bg-snow border border-muted-slate/20 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all resize-none mb-4"
            placeholder="انسخ وصف الوظيفة هنا..."
          />

          <label className="block font-bold text-text-dark mb-2 text-sm">أسئلة العميل الإضافية (اختياري)</label>
          <textarea
            value={screeningQuestions}
            onChange={(e) => setScreeningQuestions(e.target.value)}
            className="w-full h-24 p-3 bg-bg-snow border border-muted-slate/20 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all resize-none"
            placeholder="انسخ الأسئلة هنا..."
          />

          {error && (
            <div className="mt-4 p-3 bg-accent-coral/10 text-accent-coral rounded-lg flex items-center gap-2 text-sm">
              <AlertCircle size={16} /> {error}
            </div>
          )}

          <div className="mt-6">
             <button
              onClick={handleGenerate}
              disabled={loading || !jobDescription}
              className="w-full bg-primary text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-primary/90 transition-all disabled:opacity-50 shadow-lg shadow-primary/20"
            >
              {loading ? <Sparkles className="animate-spin" /> : <Send size={20} />}
              {loading ? 'جاري التحليل والتوليد...' : 'توليد العرض الاحترافي'}
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
                <BrainCircuit className="text-primary" /> العرض الذكي المولد
              </h3>
              <button
                onClick={copyToClipboard}
                className="p-2 hover:bg-bg-snow rounded-lg transition-colors flex items-center gap-2 text-sm text-primary font-medium"
              >
                {copied ? <Check size={18} /> : <Copy size={18} />}
                {copied ? 'تم النسخ' : 'نسخ العرض'}
              </button>
            </div>
            <div className="prose max-w-none text-text-dark whitespace-pre-wrap leading-relaxed text-sm md:text-base">
              {proposal}
            </div>
          </motion.section>
        )}
      </div>

      <div className="space-y-6">
        <section className="bg-white p-6 rounded-2xl shadow-sm border border-muted-slate/10 text-center">
          <h3 className="font-bold text-text-dark mb-4">Market Fit Score</h3>
          <div className="w-48 h-24 mx-auto relative">
            <Doughnut data={chartData} options={{ cutout: '80%', plugins: { tooltip: { enabled: false } } }} />
            <div className="absolute inset-0 flex items-end justify-center pb-2">
              <span className="text-3xl font-bold text-primary">{score || 0}%</span>
            </div>
          </div>
          <p className="text-sm text-muted-slate mt-4">
            {score && score > 70
              ? 'مهاراتك تطابق متطلبات الوظيفة بنسبة عالية جداً!'
              : 'يمكنك تحسين مهاراتك لزيادة نسبة القبول.'}
          </p>
        </section>

        <section className="bg-accent-coral/5 p-6 rounded-2xl border border-accent-coral/10">
          <h4 className="text-accent-coral font-bold flex items-center gap-2 mb-2">
            <Sparkles size={18} /> فجوة معرفية مكتشفة
          </h4>
          <p className="text-sm text-muted-slate mb-4">
            تحتاج الوظيفة لخبرة موثقة في تقنية معينة. هل تود إثبات كفاءتك؟
          </p>
          <button className="w-full py-2 bg-accent-coral text-white rounded-lg font-medium hover:bg-accent-coral/90 transition-colors shadow-sm">
            بدء الاختبار الذكي
          </button>
        </section>
      </div>
    </div>
  );
}
