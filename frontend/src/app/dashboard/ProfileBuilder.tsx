'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileUp, Link as LinkIcon, UserPlus } from 'lucide-react';

export default function ProfileBuilder() {
  const [method, setMethod] = useState<'pdf' | 'link' | 'manual'>('pdf');

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-muted-slate/10">
      <h3 className="text-xl font-bold text-text-dark mb-6">بناء ملفك الشخصي الصادق</h3>

      <div className="flex gap-4 mb-8">
        {[
          { id: 'pdf', icon: FileUp, label: 'رفع Resume' },
          { id: 'link', icon: LinkIcon, label: 'رابط LinkedIn' },
          { id: 'manual', icon: UserPlus, label: 'إدخال يدوي' },
        ].map((item) => (
          <button
            key={item.id}
            onClick={() => setMethod(item.id as any)}
            className={`flex-1 p-4 rounded-xl border-2 transition-all flex flex-col items-center gap-2 ${
              method === item.id
                ? 'border-primary bg-primary/5 text-primary'
                : 'border-bg-snow text-muted-slate'
            }`}
          >
            <item.icon size={24} />
            <span className="font-medium">{item.label}</span>
          </button>
        ))}
      </div>

      <div className="min-h-[200px] flex items-center justify-center border-2 border-dashed border-bg-snow rounded-2xl">
        {method === 'pdf' && (
          <div className="text-center">
            <p className="text-muted-slate mb-4">اسحب ملف الـ PDF هنا</p>
            <input type="file" className="hidden" id="pdf-upload" accept=".pdf" />
            <label htmlFor="pdf-upload" className="bg-primary text-white px-6 py-2 rounded-lg cursor-pointer">اختر ملف</label>
          </div>
        )}

        {method === 'link' && (
          <div className="w-full max-w-md px-6">
             <p className="text-muted-slate text-center mb-4">انسخ نص بروفايلك من LinkedIn أو Upwork هنا</p>
             <textarea
               className="w-full h-32 p-3 bg-bg-snow rounded-xl border border-muted-slate/20 outline-none"
               placeholder="الصق النص هنا..."
             />
             <button className="w-full mt-4 bg-primary text-white py-2 rounded-lg">تحليل النص</button>
          </div>
        )}

        {method === 'manual' && <p>النموذج اليدوي قيد التطوير...</p>}
      </div>
    </div>
  );
}
