'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Brain, CheckCircle2, AlertCircle, FileText, Send, Sparkles } from 'lucide-react';

export default function Dashboard() {
  const [jobDesc, setJobDesc] = useState('');
  const [skills, setSkills] = useState('Python, FastAPI, React');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || '/api/v1';

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          freelancer_skills: skills.split(',').map(s => s.trim()),
          job_description: jobDesc
        }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert('خطأ في الاتصال بالخادم. يرجى التأكد من تشغيل API.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans pb-20">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2 space-x-reverse">
            <div className="bg-red-600 p-2 rounded-lg">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-black tracking-tight">VeriPitch</span>
          </div>
          <div className="flex items-center space-x-4 space-x-reverse">
            <div className="w-10 h-10 rounded-full bg-slate-200 border-2 border-white shadow-sm flex items-center justify-center overflow-hidden">
              <span className="text-sm font-bold text-slate-500">M</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 mt-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-10 text-center md:text-right"
        >
          <h1 className="text-3xl font-extrabold text-slate-900 mb-3">لوحة التحكم الذكية</h1>
          <p className="text-slate-500">قم بمطابقة مهاراتك وصياغة عرضك الاحترافي في ثوانٍ.</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Input Section */}
          <section className="lg:col-span-2 space-y-6">
            <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
              <div className="flex items-center mb-6 text-slate-800">
                <Brain className="w-5 h-5 ml-2 text-red-600" />
                <h2 className="text-lg font-bold">مهاراتك الحالية</h2>
              </div>
              <input
                type="text"
                value={skills}
                onChange={(e) => setSkills(e.target.value)}
                placeholder="بايثون، رياكت، تصميم واجهات..."
                className="w-full px-5 py-4 rounded-2xl bg-slate-50 border-none focus:ring-2 focus:ring-red-500/20 text-slate-900 transition-all outline-none"
              />
            </div>

            <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
              <div className="flex items-center mb-6 text-slate-800">
                <FileText className="w-5 h-5 ml-2 text-red-600" />
                <h2 className="text-lg font-bold">وصف الوظيفة المستهدفة</h2>
              </div>
              <textarea
                rows="10"
                value={jobDesc}
                onChange={(e) => setJobDesc(e.target.value)}
                placeholder="انسخ وصف الوظيفة من Upwork أو LinkedIn هنا..."
                className="w-full px-5 py-4 rounded-2xl bg-slate-50 border-none focus:ring-2 focus:ring-red-500/20 text-slate-900 transition-all outline-none resize-none"
              ></textarea>
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full mt-6 bg-red-600 hover:bg-red-700 text-white font-bold py-4 rounded-2xl transition-all shadow-lg shadow-red-600/20 flex items-center justify-center space-x-2 space-x-reverse disabled:opacity-50"
              >
                {loading ? (
                  <span className="flex items-center">جاري التحليل...</span>
                ) : (
                  <>
                    <Search className="w-5 h-5" />
                    <span>تحليل ومطابقة المهارات</span>
                  </>
                )}
              </button>
            </div>
          </section>

          {/* Results Section */}
          <section className="lg:col-span-1">
            <AnimatePresence mode="wait">
              {!result ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="bg-white/50 border-2 border-dashed border-slate-300 rounded-3xl p-10 flex flex-col items-center justify-center text-center h-full min-h-[400px]"
                >
                  <div className="bg-slate-200 p-4 rounded-full mb-4">
                    <Send className="w-8 h-8 text-slate-400" />
                  </div>
                  <p className="text-slate-400 font-medium">ابدأ التحليل لتظهر النتائج هنا</p>
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="space-y-6"
                >
                  {/* Matching Skills */}
                  <div className="bg-white p-6 rounded-3xl shadow-sm border border-green-100">
                    <div className="flex items-center mb-4 text-green-700">
                      <CheckCircle2 className="w-5 h-5 ml-2" />
                      <h3 className="font-bold">مهارات متطابقة</h3>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {result.matched?.length > 0 ? result.matched.map((s, i) => (
                        <span key={i} className="bg-green-50 text-green-700 px-3 py-1 rounded-full text-xs font-bold border border-green-200 uppercase">{s}</span>
                      )) : <span className="text-slate-400 text-sm italic">لا يوجد تطابق</span>}
                    </div>
                  </div>

                  {/* Missing Skills */}
                  <div className="bg-white p-6 rounded-3xl shadow-sm border border-amber-100">
                    <div className="flex items-center mb-4 text-amber-700">
                      <AlertCircle className="w-5 h-5 ml-2" />
                      <h3 className="font-bold">فجوات مهارية</h3>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {result.missing?.length > 0 ? result.missing.map((s, i) => (
                        <span key={i} className="bg-amber-50 text-amber-700 px-3 py-1 rounded-full text-xs font-bold border border-amber-200 uppercase">{s}</span>
                      )) : <span className="text-slate-400 text-sm italic">لا توجد فجوات</span>}
                    </div>
                  </div>

                  {/* Proposal Card */}
                  <div className="bg-slate-900 p-8 rounded-3xl shadow-xl text-white relative overflow-hidden group">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-red-600/10 rounded-full -mr-10 -mt-10 blur-2xl" />
                    <h3 className="text-lg font-bold mb-4 relative z-10 flex items-center">
                      <Sparkles className="w-4 h-4 ml-2 text-red-500" />
                      العرض المقترح
                    </h3>
                    <p className="text-slate-300 text-sm leading-relaxed mb-6 relative z-10">
                      مرحباً، لقد قرأت متطلبات الوظيفة بعناية. أنا أمتلك خبرة قوية في {result.matched?.join(' و ')}.
                      لقد عملت سابقاً على مشاريع مشابهة تطلبت هذه المهارات، وأنا واثق من قدرتي على تقديم قيمة مضافة لمشروعكم.
                    </p>
                    <button className="w-full bg-white text-slate-900 font-bold py-3 rounded-xl hover:bg-slate-100 transition-colors relative z-10 flex items-center justify-center space-x-2 space-x-reverse">
                      <span>نسخ العرض</span>
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </section>
        </div>
      </main>
    </div>
  );
}
