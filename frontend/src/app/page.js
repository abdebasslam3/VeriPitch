'use client';

import React from 'react';

export default function LoginPage() {
  const WHOP_APP_ID = process.env.NEXT_PUBLIC_WHOP_APP_ID;

  // استخدام متغير بيئة للرابط أو تحديد رابط ديناميكي
  const getRedirectUri = () => {
    if (typeof window !== 'undefined') {
      return `${window.location.origin}/api/auth/whop`;
    }
    return "http://localhost:3000/api/auth/whop";
  };

  const REDIRECT_URL = getRedirectUri();

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      fontFamily: 'sans-serif',
      direction: 'rtl'
    }}>
      <h1>مرحباً بك في VeriPitch</h1>
      <p>سجل دخولك عبر Whop للبدء في صياغة عروضك الاحترافية</p>

      <a
        href={`https://whop.com/oauth/authorize?client_id=${WHOP_APP_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URL)}&response_type=code&scope=user_profile%20memberships`}
        style={{
          backgroundColor: '#ff5a5f',
          color: 'white',
          padding: '12px 24px',
          borderRadius: '8px',
          textDecoration: 'none',
          fontWeight: 'bold',
          marginTop: '20px'
        }}
      >
        تسجيل الدخول عبر Whop
      </a>
    </div>
  );
}
