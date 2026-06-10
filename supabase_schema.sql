-- تفعيل إضافات الحماية وتوليد المعرفات الفرعية
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- جدول المستخدمين والتحقق من اشتراك Whop الصارم (مرتبط بـ auth.users الخاص بـ Supabase)
-- جدول المستخدمين والتحقق من اشتراك Whop الصارم
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    whop_user_id TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    subscription_status TEXT DEFAULT 'active' CHECK (subscription_status IN ('active', 'inactive', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- جدول ملف الفريلانسر الموثق (The Source of Truth)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL UNIQUE,
    bio_summary TEXT,
    skills JSONB DEFAULT '[]'::jsonb,      -- الهيكل: [{"name": "React", "verified": true, "source": "quiz"}]
    portfolio JSONB DEFAULT '[]'::jsonb,   -- الهيكل: [{"title": "SaaS", "url": "...", "description": "..."}]
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- جدول تاريخ العروض المولدة وإجابات الأسئلة مع حفظ مؤشر الجاهزية تاريخياً لكل وظيفة
CREATE TABLE IF NOT EXISTS proposals_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    job_title TEXT NOT NULL,
    job_description TEXT NOT NULL,
    generated_proposal TEXT NOT NULL,
    screening_answers JSONB DEFAULT '[]'::jsonb,
    used_model TEXT NOT NULL CHECK (used_model IN ('gemini', 'claude')),
    market_fit_score INT NOT NULL,         -- مضافة لحفظ النتيجة التاريخية للطلب
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- جدول فترات قفل الاختبارات الذكية لمدة ساعتين (منع التلاعب من جهة السيرفر)
CREATE TABLE IF NOT EXISTS quiz_cooldowns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    skill_name TEXT NOT NULL,
    locked_until TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    UNIQUE(user_id, skill_name)
);

-- الفهارس لرفع أداء الاستعلامات وفحص القيود بسرعة عالية
CREATE INDEX IF NOT EXISTS idx_proposals_user ON proposals_history(user_id);
CREATE INDEX IF NOT EXISTS idx_cooldowns_lookup ON quiz_cooldowns(user_id, skill_name, locked_until);
