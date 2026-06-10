'use client';

import React, { useState, useEffect } from 'react';
import { Save, Shield, Key } from 'lucide-react';

export default function SettingsView() {
  const [geminiKey, setGeminiKey] = useState('');
  const [claudeKey, setClaudeKey] = useState('');
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    setGeminiKey(localStorage.getItem('GEMINI_API_KEY') || '');
    setClaudeKey(localStorage.getItem('CLAUDE_API_KEY') || '');
  }, []);

  const handleSave = () => {
    localStorage.setItem('GEMINI_API_KEY', geminiKey);
    localStorage.setItem('CLAUDE_API_KEY', claudeKey);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-muted-slate/10 max-w-2xl">
      <h3 className="text-xl font-bold text-text-dark mb-6 flex items-center gap-2">
        <Shield className="text-primary" /> إعدادات الحماية (Zero-Knowledge)
      </h3>

      <p className="text-sm text-muted-slate mb-6">
        يتم تشفير مفاتيح API الخاصة بك محلياً في متصفحك. نحن لا نقوم بحفظها أبداً في قواعد بياناتنا.
      </p>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-bold text-text-dark mb-2 flex items-center gap-2">
            <Key size={14} /> Gemini API Key
          </label>
          <input
            type="password"
            value={geminiKey}
            onChange={(e) => setGeminiKey(e.target.value)}
            className="w-full p-3 bg-bg-snow border border-muted-slate/20 rounded-xl outline-none focus:ring-2 focus:ring-primary/20"
            placeholder="sk-..."
          />
        </div>

        <div>
          <label className="block text-sm font-bold text-text-dark mb-2 flex items-center gap-2">
            <Key size={14} /> Claude API Key
          </label>
          <input
            type="password"
            value={claudeKey}
            onChange={(e) => setClaudeKey(e.target.value)}
            className="w-full p-3 bg-bg-snow border border-muted-slate/20 rounded-xl outline-none focus:ring-2 focus:ring-primary/20"
            placeholder="sk-ant-..."
          />
        </div>

        <button
          onClick={handleSave}
          className="w-full bg-primary text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-primary/90 transition-all shadow-lg shadow-primary/10 mt-4"
        >
          <Save size={20} />
          {saved ? 'تم الحفظ بأمان' : 'حفظ المفاتيح مشفرة'}
        </button>
      </div>
    </div>
  );
}
