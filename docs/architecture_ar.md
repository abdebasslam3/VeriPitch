# البنية التقنية لمشروع VeriPitch (Proposed Architecture)

## 1. المنهجية الأساسية: RAG (Retrieval-Augmented Generation)
لتحقيق هدف "الصدق بنسبة 100%" ومنع "الهلوسة"، نعتمد تقنية RAG لضمان أن كل كلمة في العرض مستمدة من حقيقة موجودة في ملف المستقل.

## 2. التكامل مع منصة Whop (Whop Integration)
تم دمج منصة Whop لإدارة الاشتراكات والتحقق من هوية المستخدمين:
- **Authentication:** يتم استخدام Whop OAuth 2.0 لتسجيل دخول المستخدمين.
- **Membership Management:** يقوم `WhopClient` في الخلفية بالتحقق من حالة اشتراك المستخدم قبل السماح له بتوليد العروض.
- **Frontend:** تطبيق Next.js يتفاعل مع Whop SDK لتسهيل عملية الدفع والوصول.

## 3. المكونات التقنية المحدثة (Refined Tech Stack)
- **Backend:** Python / FastAPI / Whop API Client.
- **Frontend:** Next.js (React) / Whop SDK.
- **Security:** إدارة متغيرات البيئة عبر `.env` (WHOP_API_KEY).

## 4. تدفق التحقق من الوصول (Authorization Flow)
1. يسجل المستخدم دخوله عبر Whop في الواجهة الأمامية.
2. ترسل الواجهة الـ User ID إلى الخلفية.
3. يقوم الـ `WhopClient` بطلب العضويات من API الخاص بـ Whop.
4. إذا كان لدى المستخدم اشتراك نشط، يتم تفعيل ميزات الذكاء الاصطناعي له.
