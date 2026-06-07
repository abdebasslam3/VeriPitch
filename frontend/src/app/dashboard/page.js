'use client';

import React, { useState } from 'react';

export default function Dashboard() {
  const [jobDesc, setJobDesc] = useState('');
  const [skills, setSkills] = useState('Python, FastAPI, React');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/analyze', {
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
      alert('خطأ في الاتصال بالخادم');
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif', direction: 'rtl', maxWidth: '800px', margin: '0 auto' }}>
      <h1>لوحة التحكم - VeriPitch</h1>

      <div style={{ marginBottom: '20px' }}>
        <label>مهاراتك (افصل بينها بفاصلة):</label><br/>
        <input
          type="text"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          style={{ width: '100%', padding: '10px', marginTop: '5px' }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label>وصف الوظيفة:</label><br/>
        <textarea
          rows="10"
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
          style={{ width: '100%', padding: '10px', marginTop: '5px' }}
          placeholder="انسخ وصف الوظيفة هنا..."
        ></textarea>
      </div>

      <button
        onClick={handleAnalyze}
        disabled={loading}
        style={{
          backgroundColor: '#0070f3',
          color: 'white',
          padding: '10px 20px',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
      >
        {loading ? 'جاري التحليل...' : 'تحليل الوظيفة ومطابقة المهارات'}
      </button>

      {result && (
        <div style={{ marginTop: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '10px' }}>
          <h3>النتيجة:</h3>
          <p>✅ <strong>المهارات المتطابقة:</strong> {result.matched?.join(', ') || 'لا يوجد'}</p>
          <p>⚠️ <strong>المهارات الناقصة:</strong> {result.missing?.join(', ') || 'لا يوجد'}</p>

          <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f0f7ff', borderRadius: '5px' }}>
            <h4>عرض العمل المقترح (صادق 100%):</h4>
            <p style={{ whiteSpace: 'pre-wrap' }}>
              مرحباً، لقد قرأت متطلبات الوظيفة بعناية. أنا أمتلك خبرة قوية في {result.matched?.join(' و ')}.
              لقد عملت سابقاً على مشاريع مشابهة تطلبت هذه المهارات، وأنا واثق من قدرتي على تقديم قيمة مضافة لمشروعكم.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
